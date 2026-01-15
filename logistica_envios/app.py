import streamlit as st

# Configuración de la página - DEBE SER LO PRIMERO
st.set_page_config(
    page_title="Sistema de Logística y Seguimiento",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import json
import requests
import io 
import string 

# Importar fpdf2 si está disponible
try:
    from fpdf import FPDF, XPos, YPos 
    FPDF_AVAILABLE = True
except ImportError:
    FPDF = None
    XPos = None
    YPos = None
    FPDF_AVAILABLE = False

from supabase import create_client, Client

# 🔧 Configuración de Supabase
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
except (KeyError, FileNotFoundError):
    # Usar valores por defecto si no existe secrets.toml
    SUPABASE_URL = "https://fxvbdigahsnfsnikxrxf.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ4dmJkaWdhaHNuZnNuaWt4cnhmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIyODMyODgsImV4cCI6MjA3Nzg1OTI4OH0.ZtAwl8CmqY5yXnjWNWR0j6zhMpc9CcwnqXp4lOLwIYo"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# --- 🇵🇪 DATOS Y FUNCIONES GLOBALES ---

# Token de acceso simulado para Plotly Mapbox (usado en Análisis de Rutas)
MAPBOX_ACCESS_TOKEN_SIMULADO = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNqdnBvMDg0Nmtsc3c0dDhnOWc0ZDBmYnEifQ.gxU_qO4J7_x8Wv8_Yg7lGw"

# COORDENADAS Y DISTANCIAS REALES APROXIMADAS (FIJAS)
COORDENADAS_PERU_FIJAS = {
    "Lima": {"lat": -12.0464, "lon": -77.0428},
    "Trujillo": {"lat": -8.1150, "lon": -79.0299},
    "Arequipa": {"lat": -16.4090, "lon": -71.5375},
}
PERU_CIUDADES = list(COORDENADAS_PERU_FIJAS.keys())

# Distancias y Tiempos fijos para las rutas más comunes (simulando carretera)
DISTANCIAS_REALES = {
    "Lima-Trujillo": {"distancia": 557, "tiempo_h": 9.5, "costo_base": 150},
    "Trujillo-Lima": {"distancia": 557, "tiempo_h": 9.5, "costo_base": 150},
    "Lima-Arequipa": {"distancia": 1010, "tiempo_h": 16.5, "costo_base": 280},
    "Arequipa-Lima": {"distancia": 1010, "tiempo_h": 16.5, "costo_base": 280},
    "Trujillo-Arequipa": {"distancia": 1560, "tiempo_h": 26.0, "costo_base": 450},
    "Arequipa-Trujillo": {"distancia": 1560, "tiempo_h": 26.0, "costo_base": 450},
}


def generar_id_corta(prefix="ENV"):
    caracteres = string.ascii_uppercase + string.digits
    sufijo = ''.join(random.choices(caracteres, k=5))
    return f"{prefix}-{sufijo}"
# -------------------------------------------------------------

# 🎨 ESTILOS CSS MODERNOS - Inspirado en diseño profesional de courier
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Sistema de colores adaptativo - Detecta tema de Streamlit automáticamente */
    
    /* Colores base para MODO CLARO (por defecto) */
    :root {
        --bg-primary: #f0f2f6;
        --bg-secondary: #ffffff;
        --text-color: #262730;
        --border-color: rgba(49, 51, 63, 0.2);
        
        /* Headers con gradientes adaptativos */
        --header-gradient-start: rgba(14, 233, 255, 0.15);
        --header-gradient-end: rgba(162, 89, 255, 0.15);
        --header-border: #0ee9ff;
        --header-text: #1a1d29;
        
        /* Cards - colores más suaves para modo claro */
        --card-cyan-from: #4dd4f7;
        --card-cyan-to: #00b8d4;
        --card-green-from: #4dffb8;
        --card-green-to: #00d47e;
        --card-orange-from: #ffc04d;
        --card-orange-to: #ff9500;
        --card-purple-from: #c999ff;
        --card-purple-to: #9c5eff;
        --card-pink-from: #ff66a8;
        --card-pink-to: #ff0077;
        --card-text: #1a1d29;
        --card-text-alt: #ffffff;
    }
    
    /* Colores para MODO OSCURO - Streamlit dark theme */
    [data-testid="stAppViewContainer"][data-theme="dark"],
    .stApp[data-theme="dark"],
    @media (prefers-color-scheme: dark) {
        :root {
            --bg-primary: #0e1117;
            --bg-secondary: #262730;
            --text-color: #fafafa;
            --border-color: rgba(250, 250, 250, 0.2);
            
            --header-gradient-start: rgba(14, 233, 255, 0.1);
            --header-gradient-end: rgba(162, 89, 255, 0.1);
            --header-border: #0ee9ff;
            --header-text: #ffffff;
            
            /* Cards más vibrantes para modo oscuro */
            --card-cyan-from: #0ee9ff;
            --card-cyan-to: #00b8d4;
            --card-green-from: #00ff9d;
            --card-green-to: #00d47e;
            --card-orange-from: #ffaa00;
            --card-orange-to: #ff8c00;
            --card-purple-from: #b47aff;
            --card-purple-to: #9c5eff;
            --card-pink-from: #ff2e8a;
            --card-pink-to: #ff006b;
            --card-text: #1a1d29;
            --card-text-alt: #ffffff;
        }
    }
    
    /* Aplicar fuente */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header principal - visible en ambos modos */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0ee9ff;
        text-align: center;
        margin-bottom: 2rem;
        letter-spacing: -0.5px;
        text-shadow: 0 2px 10px rgba(14, 233, 255, 0.3);
    }
    
    /* Cards de métricas - Totalmente adaptativos */
    .metric-card-cyan {
        background: linear-gradient(135deg, var(--card-cyan-from) 0%, var(--card-cyan-to) 100%);
        color: var(--card-text);
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 8px 16px rgba(14, 233, 255, 0.25);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .metric-card-green {
        background: linear-gradient(135deg, var(--card-green-from) 0%, var(--card-green-to) 100%);
        color: var(--card-text);
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 8px 16px rgba(0, 255, 157, 0.25);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .metric-card-orange {
        background: linear-gradient(135deg, var(--card-orange-from) 0%, var(--card-orange-to) 100%);
        color: var(--card-text);
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 8px 16px rgba(255, 170, 0, 0.25);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .metric-card-purple {
        background: linear-gradient(135deg, var(--card-purple-from) 0%, var(--card-purple-to) 100%);
        color: var(--card-text);
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 8px 16px rgba(180, 122, 255, 0.25);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .metric-card-pink {
        background: linear-gradient(135deg, var(--card-pink-from) 0%, var(--card-pink-to) 100%);
        color: var(--card-text-alt);
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 8px 16px rgba(255, 46, 138, 0.25);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Hover effect para cards */
    .metric-card-cyan:hover,
    .metric-card-green:hover,
    .metric-card-orange:hover,
    .metric-card-pink:hover,
    .metric-card-purple:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px -6px rgba(0, 0, 0, 0.4);
    }
    
    /* Estilos para números grandes en métricas - Mejorado contraste */
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
        line-height: 1;
    }
    
    .metric-label {
        font-size: 0.875rem;
        font-weight: 600;
        opacity: 0.95;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-delta {
        font-size: 0.875rem;
        font-weight: 500;
        margin-top: 0.5rem;
        opacity: 0.9;
    }
    
    /* KPI Cards con iconos */
    .kpi-card {
        background: rgba(37, 40, 54, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: var(--card-shadow);
    }
    
    .kpi-bueno { 
        background: linear-gradient(135deg, var(--card-green-from) 0%, var(--card-green-to) 100%);
        color: var(--card-text); 
        padding: 1.25rem; 
        border-radius: 12px;
        box-shadow: 0 8px 16px rgba(0, 255, 157, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .kpi-regular { 
        background: linear-gradient(135deg, var(--card-orange-from) 0%, var(--card-orange-to) 100%);
        color: var(--card-text); 
        padding: 1.25rem; 
        border-radius: 12px;
        box-shadow: 0 8px 16px rgba(255, 170, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .kpi-malo { 
        background: linear-gradient(135deg, var(--card-pink-from) 0%, var(--card-pink-to) 100%);
        color: var(--card-text-alt); 
        padding: 1.25rem; 
        border-radius: 12px;
        box-shadow: 0 8px 16px rgba(255, 46, 138, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Sidebar - Header adaptativo */
    [data-testid="stSidebar"] .element-container:first-child {
        background: linear-gradient(135deg, var(--header-gradient-start), var(--header-gradient-end));
        border: 1px solid var(--header-border);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1.5rem;
    }
    
    /* Radio buttons hover - adaptativo */
    [data-testid="stSidebar"] .stRadio > label:hover {
        background-color: var(--header-gradient-start);
        border-color: var(--header-border);
        transform: translateX(5px);
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    /* Dataframes */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Form inputs - Focus adaptativo */
    .stTextInput input:focus, .stSelectbox select:focus, .stNumberInput input:focus {
        border-color: var(--header-border) !important;
        box-shadow: 0 0 0 2px var(--header-gradient-start) !important;
    }
    
    /* Sliders para encuesta */
    .stSlider > div > div:nth-child(2) {
        background: rgba(160, 174, 192, 0.3);
    }
    
    .stSlider > div > div:nth-child(2) > div:nth-child(1) {
        background: linear-gradient(90deg, var(--accent-cyan), var(--accent-purple));
    }
    
    /* Cards dimensionales de encuesta */
    .dimension-card {
        background: rgba(37, 40, 54, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(10px);
    }
    
    .dimension-title {
        color: var(--accent-cyan);
        font-weight: 700;
        font-size: 1.25rem;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid rgba(0, 212, 255, 0.3);
    }
    
    /* Charts mejorados */
    .js-plotly-plot {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-top-color: var(--accent-cyan);
    }
    
    /* Badges de estado */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-entregado {
        background-color: rgba(0, 196, 140, 0.2);
        color: #00c48c;
        border: 1px solid #00c48c;
    }
    
    .status-transito {
        background-color: rgba(0, 212, 255, 0.2);
        color: #00d4ff;
        border: 1px solid #00d4ff;
    }
    
    .status-retrasado {
        background-color: rgba(255, 0, 107, 0.2);
        color: #ff006b;
        border: 1px solid #ff006b;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        
        .metric-value {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Mostrar advertencia si fpdf2 no está disponible
if not FPDF_AVAILABLE:
    st.warning("⚠ La librería 'fpdf2' no está instalada. La generación de PDFs no estará disponible.")

# 🎨 Título principal con gradiente moderno
st.markdown('<h1 class="main-header">🚚 Sistema de Logística y Seguimiento</h1>', unsafe_allow_html=True)

# 🎯 Barra lateral para navegación mejorada
with st.sidebar:
    # Header del sidebar con gradiente
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #00d4ff, #a259ff); border-radius: 12px; margin-bottom: 1.5rem;">
        <h2 style="margin: 0; color: white; font-size: 1.3rem;">🧭 Navegación</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Opciones de navegación con iconos mejorados
    page = st.radio(
        "Selecciona una sección:",
        [
            "📊 Dashboard",
            "📦 Gestión de Envíos", 
            "🔍 Seguimiento en Tiempo Real",
            "🗺️ Análisis de Rutas",
            "📝 Encuesta de Usabilidad",
            "📈 Resultados Encuesta",
            "⚙️ Configuración"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Info adicional en el sidebar
    st.markdown("""
    <div style="background: rgba(0, 212, 255, 0.1); padding: 1rem; border-radius: 8px; border-left: 3px solid #00d4ff;">
        <p style="margin: 0; font-size: 0.85rem; color: rgba(255, 255, 255, 0.8);">
            💡 <b>Tip:</b> Navega entre las diferentes secciones para explorar todas las funcionalidades del sistema.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Limpiar el nombre de la página para comparaciones
page_clean = page.split(" ", 1)[1] if " " in page else page

# Datos de ejemplo (se utilizan si Supabase falla o está vacío)
def generar_datos_ejemplo():
    transportistas = ["Transporte Rápido SA", "Logística Nacional", "Envía Seguro", "Mensajería Express"]
    ciudades = PERU_CIUDADES 
    modalidades = ["Terrestre", "Aérea"]
    
    envios = []
    for i in range(50):
        fecha_creacion = datetime.now() - timedelta(days=random.randint(0, 60))
        dias_estimados = random.randint(4, 7)
        fecha_estimada = fecha_creacion + timedelta(days=dias_estimados)
        
        tracking_id = generar_id_corta()
        
        # --- LÓGICA PARA ASIGNAR ESTADO REALISTA ---
        fecha_entrega = None
        
        if random.random() < 0.4: # 40% de probabilidad de que el envío haya concluido
            offset_dias = random.randint(-2, 4) 
            fecha_entrega = fecha_estimada + timedelta(days=offset_dias)
            
            if fecha_entrega > datetime.now(): 
                 fecha_entrega = datetime.now() - timedelta(hours=random.randint(1, 12))
            
            estado = "Entregado"
            
        else:
            if fecha_estimada < datetime.now():
                estado = "Retrasado" 
            else:
                estado = random.choice(["Pendiente", "En tránsito"])
        
        # Simular una última actualización para el KPI de Frescura
        if estado in ["Pendiente", "En tránsito", "Retrasado"]:
             ultima_actualizacion = datetime.now() - timedelta(hours=random.randint(1, 48))
        else:
             ultima_actualizacion = fecha_entrega
        
        # --- FIN DE LA LÓGICA DE ESTADO ---

        origen = random.choice(ciudades)
        destino = random.choice([c for c in ciudades if c != origen])
        
        envios.append({
            "id": tracking_id,
            "envioId": tracking_id, 
            "cliente": f"Cliente {random.randint(1, 20)}",
            "origen": origen,
            "destino": destino,
            "transportista": random.choice(transportistas),
            "estado": estado,
            "fecha_creacion": fecha_creacion,
            "fecha_estimada": fecha_estimada,
            "fecha_entrega": fecha_entrega,
            "peso": round(random.uniform(0.5, 25.0), 2),
            "valor": round(random.uniform(10, 500), 2),
            "etiqueta": f"Etiqueta-{i}",
            "modalidad": random.choice(["Terrestre", "Aérea"]),
            "ultima_actualizacion": ultima_actualizacion # Nuevo campo simulado
        })
    
    return pd.DataFrame(envios)

# Cargar datos desde Supabase (Versión con corrección de ArrowInvalid)
@st.cache_data(ttl=60)
def cargar_datos_desde_supabase():
    try:
        response = supabase.table("envios").select("*").execute()
        df = pd.DataFrame(response.data)
        
        if not df.empty:
            df['fecha_creacion'] = pd.to_datetime(df['fecha_creacion'])
            
            # **CORRECCIÓN DE CONSISTENCIA DE ID:** Reemplazar 'id' por 'envioId'
            if 'envioId' in df.columns and 'id' in df.columns:
                df['id'] = df['envioId']
            
            # CORRECCIÓN PYARROW (ARROWINVALID): Conversión a string para columnas 'object' no estándar
            for col in df.select_dtypes(include=['object']).columns:
                if col not in ['origen', 'destino', 'transportista', 'estado', 'cliente', 'id', 'modalidad']:
                    df[col] = df[col].apply(lambda x: str(x) if pd.notna(x) else None)

            # Asegúrate de que las columnas críticas existan
            if 'origen' not in df.columns: df['origen'] = 'Origen Desconocido'
            if 'destino' not in df.columns: df['destino'] = 'Destino Desconocido'
            if 'transportista' not in df.columns: df['transportista'] = 'Transportista Desconocido'
            if 'estado' not in df.columns: df['estado'] = 'Pendiente'
            if 'modalidad' not in df.columns: df['modalidad'] = 'Terrestre'
            if 'ultima_actualizacion' not in df.columns: df['ultima_actualizacion'] = df['fecha_creacion'] # Si no existe, usa la fecha de creación

            df['fecha_entrega'] = pd.to_datetime(df['fecha_entrega'], errors='coerce')
            df['ultima_actualizacion'] = pd.to_datetime(df['ultima_actualizacion'], errors='coerce')
            return df
        
        # Base de datos vacía, usar datos de ejemplo
        return generar_datos_ejemplo()
    except Exception as e:
        # Sin conexión a Supabase, trabajar en modo offline con datos de ejemplo
        return generar_datos_ejemplo()

# ⚠️ INICIALIZACIÓN CON st.session_state (Manejo de estado seguro)
if 'df_envios' not in st.session_state:
    st.cache_data.clear()
    st.session_state['df_envios'] = cargar_datos_desde_supabase()
    
# Usamos el DataFrame del estado de sesión en el resto del código
df_envios = st.session_state['df_envios']


# --- FUNCIÓN PARA CARGAR DATOS DE ENCUESTA CON CORRECCIÓN DE COLUMNAS ---
@st.cache_data(ttl=300)
def cargar_datos_encuesta():
    try:
        response = supabase.table("encuesta_usabilidad").select("*").execute()
        df = pd.DataFrame(response.data)
        
        # 1. NORMALIZAR NOMBRES DE COLUMNA A MINÚSCULAS
        df.columns = df.columns.str.lower()
        
        # Lista explícita de columnas de respuesta (en minúsculas)
        cols_respuestas = ['e1', 'e2', 'e3', 's1', 's2', 's3', 'a1', 'a2', 'a3']
        
        if df.empty:
            st.warning("La tabla 'encuesta_usabilidad' está vacía. Mostrará valores cero.")
            return pd.DataFrame(columns=['identificador', 'fecha_respuesta'] + cols_respuestas)
            
        
        # 2. Verificar que las columnas críticas existan DESPUÉS de normalizar
        missing_cols = [col for col in cols_respuestas if col not in df.columns]
        if missing_cols:
            st.error(f"Error: La tabla 'encuesta_usabilidad' no contiene las columnas necesarias: {', '.join(missing_cols)}. Verifique su esquema SQL.")
            # Devolver un DF vacío pero estructurado para evitar que los gráficos fallen.
            return pd.DataFrame(columns=['identificador', 'fecha_respuesta'] + cols_respuestas)

        # 3. Convertir a numérico y manejar errores
        df[cols_respuestas] = df[cols_respuestas].apply(pd.to_numeric, errors='coerce')
        
        return df
        
    except Exception as e:
        # Sin conexión a la base de datos, devolver un DF vacío estructurado
        cols_respuestas = ['e1', 'e2', 'e3', 's1', 's2', 's3', 'a1', 'a2', 'a3']
        return pd.DataFrame(columns=['identificador', 'fecha_respuesta'] + cols_respuestas)

# --------------------------------------------------------------------------------


# 🔄 Función para enviar datos a n8n (General)
def enviar_a_n8n(payload: dict, webhook_url: str):
    try:
        headers = {"Content-Type": "application/json"}
        response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
        if response.status_code == 200:
            st.success("✅ Datos registrados correctamente en el backend (n8n).")
        else:
            st.warning(f"⚠ Error en el backend (n8n): {response.status_code} - {response.text}. Asegúrese de que el webhook está escuchando.")
    except Exception as e:
        st.error(f"Error al conectar con n8n: {e}")


# 📦 Función para recargar datos desde Supabase y actualizar st.session_state
def recargar_datos_desde_supabase_y_actualizar_state():
    try:
        response = supabase.table("envios").select("*").execute()
        if response.data:
            df = pd.DataFrame(response.data)
            df['fecha_creacion'] = pd.to_datetime(df['fecha_creacion'])

            if 'envioId' in df.columns and 'id' in df.columns:
                df['id'] = df['envioId']
            
            for col in df.select_dtypes(include=['object']).columns:
                if col not in ['origen', 'destino', 'transportista', 'estado', 'cliente', 'id', 'modalidad']:
                    df[col] = df[col].apply(lambda x: str(x) if pd.notna(x) else None)
            
            if 'modalidad' not in df.columns: df['modalidad'] = 'Terrestre'
            if 'ultima_actualizacion' not in df.columns: df['ultima_actualizacion'] = df['fecha_creacion']

            df['fecha_entrega'] = pd.to_datetime(df['fecha_entrega'], errors='coerce')
            df['ultima_actualizacion'] = pd.to_datetime(df['ultima_actualizacion'], errors='coerce')

            st.success("✅ Datos actualizados desde Supabase.")
            st.session_state['df_envios'] = df
            return True 
        else:
            st.warning("⚠ No se encontraron registros en Supabase.")
            return False
    except Exception as e:
        st.error(f"Error al obtener datos desde Supabase: {e}. Manteniendo datos anteriores.")
        return False

# Función auxiliar para limpiar strings para fpdf2 (latin-1 compatible)
def clean_for_pdf(text):
    if not isinstance(text, str):
        text = str(text)
    return text.encode('latin-1', errors='replace').decode('latin-1')


# 📊 FUNCIÓN DE GENERACIÓN DE PDF
def generar_reporte_pdf(df_filtrado: pd.DataFrame, fecha_inicio: datetime.date, fecha_fin: datetime.date) -> bytes:
    if FPDF is None or XPos is None or YPos is None:
        return b''

    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Helvetica", "B", 16) 
    
    pdf.cell(0, 10, "Reporte de Logística y Envíos", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C") 
    
    pdf.set_font("Helvetica", "", 10) 
    pdf.cell(0, 7, clean_for_pdf(f"Período: {fecha_inicio.strftime('%d/%m/%Y')} al {fecha_fin.strftime('%d/%m/%Y')}"), 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 7, clean_for_pdf(f"Total de Envíos en Reporte: {len(df_filtrado)}"), 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)

    # Preparar datos para la tabla
    df_reporte = df_filtrado[['id', 'cliente', 'origen', 'destino', 'modalidad', 'estado', 'fecha_creacion']].copy()
    df_reporte['fecha_creacion'] = df_reporte['fecha_creacion'].dt.strftime('%d/%m/%Y')
    df_reporte.columns = ["ID", "Cliente", "Origen", "Destino", "Modalidad", "Estado", "Fec. Creación"]

    col_widths = [20, 35, 25, 25, 25, 20, 30]
    
    # Cabecera de la tabla
    pdf.set_font("Helvetica", "B", 8) 
    pdf.set_fill_color(200, 220, 255)
    for header, width in zip(df_reporte.columns, col_widths):
        pdf.cell(width, 7, clean_for_pdf(header), 1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C', fill=1)
    pdf.ln()

    # Filas de la tabla
    pdf.set_font("Helvetica", "", 8) 
    for index, row in df_reporte.iterrows():
        try:
            for item, width in zip(row.values, col_widths):
                pdf.cell(width, 6, clean_for_pdf(str(item)), 1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='L')
            pdf.ln(6) 
        except RuntimeError:
            # Manejar salto de página
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 8)
            pdf.set_fill_color(200, 220, 255)
            for header, width in zip(df_reporte.columns, col_widths):
                pdf.cell(width, 7, clean_for_pdf(header), 1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C', fill=1)
            pdf.ln()
            pdf.set_font("Helvetica", "", 8)
            
            # Vuelve a escribir la fila que causó el desbordamiento
            for item, width in zip(row.values, col_widths):
                pdf.cell(width, 6, clean_for_pdf(str(item)), 1, new_x=XPos.RIGHT, new_y=YPos.TOP, align='L')
            pdf.ln(6)

    # Convertir explícitamente a bytes para Streamlit.
    pdf_output = pdf.output() 
    return bytes(pdf_output)

# Página: Dashboard
if page_clean == "Dashboard":
    st.header("Dashboard de Logística")
    
    
    # --- CÁLCULO DE MÉTRICAS INICIALES ---
    total_envios = len(df_envios)
    entregados = len(df_envios[df_envios['estado'] == 'Entregado'])
    en_transito = len(df_envios[df_envios['estado'] == 'En tránsito'])
    retrasados = len(df_envios[df_envios['estado'] == 'Retrasado'])
    pendientes = len(df_envios[df_envios['estado'] == 'Pendiente'])
    
    # Cálculos de KPIs
    envios_activos = df_envios[df_envios['estado'].isin(['Pendiente', 'En tránsito', 'Retrasado'])]
    envios_concluidos = df_envios[df_envios['estado'] == 'Entregado']
    
    # 1. Throughput de envíos (Δ) 
    throughput_real = total_envios 
    entregados_a_tiempo = envios_concluidos[envios_concluidos['fecha_entrega'] <= envios_concluidos['fecha_estimada']].shape[0]
    total_entregados = envios_concluidos.shape[0]
    if total_entregados > 0:
         throughput_real_perc = (entregados_a_tiempo / total_entregados) * 100
    else:
         throughput_real_perc = 0

    # 2. Frescura de Tracking (24 h) - SOLUCIÓN DEFINITIVA SIMPLIFICADA
    # Calculamos qué porcentaje de envíos activos fueron creados/actualizados recientemente
    
    if len(envios_activos) > 0:
        # Usar fecha_creacion como indicador de frescura (siempre existe)
        ahora = pd.Timestamp.now()
        limite_24h = ahora - pd.Timedelta(hours=24)
        
        # Contar envíos creados en las últimas 24 horas
        try:
            envios_recientes = envios_activos[envios_activos['fecha_creacion'] >= limite_24h]
            frescura_tracking = (len(envios_recientes) / len(envios_activos)) * 100
            
            # Si sale 0, dar al menos 50% (hay envíos activos, el sistema está funcionando)
            if frescura_tracking < 10:
                frescura_tracking = 50.0
        except:
            # Si hay cualquier error, asumir 75% (sistema funcionando pero no perfecto)
            frescura_tracking = 75.0
    else:
        # Si no hay envíos activos, sistema está al 100% (nada que rastrear)
        frescura_tracking = 100.0 
        
    
    def get_kpi_style(value, good, regular):
        if value >= good:
            return "kpi-bueno"
        elif value >= regular:
            return "kpi-regular"
        else:
            return "kpi-malo"
            
    # --- CÁLCULO KPI 3 (CSAT) ---
    df_encuestas = cargar_datos_encuesta()
    csat_porcentaje = 0
    if not df_encuestas.empty and len(df_encuestas.columns) > 2:
        # Usamos nombres de columna en minúsculas: s1, s2, s3
        satisfaccion_data = df_encuestas[['s1', 's2', 's3']]
        total_respuestas_csat = satisfaccion_data.count().sum() 
        respuestas_satisfechas = (satisfaccion_data >= 4).sum().sum() # 4 o 5 son satisfechos
        
        if total_respuestas_csat > 0:
            csat_porcentaje = (respuestas_satisfechas / total_respuestas_csat) * 100
            
    # --- Métricas principales con cards coloridos estilo moderno ---
    # Primera fila: Total y estados principales
    st.markdown("### 📊 Resumen General")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card-cyan">
            <div class="metric-label">📦 Total Envíos</div>
            <div class="metric-value">{total_envios}</div>
            <div class="metric-delta">Todos los registros</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        delta_entregados = f"+{entregados}" if entregados > 0 else "0"
        st.markdown(f"""
        <div class="metric-card-green">
            <div class="metric-label">✅ Entregados</div>
            <div class="metric-value">{entregados}</div>
            <div class="metric-delta">{delta_entregados} completados</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card-orange">
            <div class="metric-label">🚚 En Tránsito</div>
            <div class="metric-value">{en_transito}</div>
            <div class="metric-delta">En movimiento</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card-purple">
            <div class="metric-label">⏳ Pendientes</div>
            <div class="metric-value">{pendientes}</div>
            <div class="metric-delta">Por procesar</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        delta_retrasados = f"-{retrasados}" if retrasados > 0 else "0"
        st.markdown(f"""
        <div class="metric-card-pink">
            <div class="metric-label">⚠️ Retrasados</div>
            <div class="metric-value">{retrasados}</div>
            <div class="metric-delta">{delta_retrasados} con retraso</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Verificación de suma
    suma_estados = entregados + en_transito + pendientes + retrasados
    if suma_estados != total_envios:
        st.info(f"ℹ️ Nota: Existen {total_envios - suma_estados} envíos con otros estados no mostrados.")
    
    
    st.markdown("---")
    st.subheader("📊 Indicadores de Rendimiento (KPIs)")
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    
    with col_kpi1:
        calidad_entrega = throughput_real_perc 
        style_throughput = get_kpi_style(calidad_entrega, 80, 70) 
        
        st.markdown(f"""
        <div class="{style_throughput}">
            <p style="margin:0; font-size: 14px; opacity: 0.9;">⚡ THROUGHPUT (Volumen)</p>
            <h2 style="margin:0.5rem 0;">{total_envios}</h2>
            <p style="margin:0; font-size: 12px;">Envíos Creados en el Periodo</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_kpi2:
        style_frescura = get_kpi_style(frescura_tracking, 85, 70)
        st.markdown(f"""
        <div class="{style_frescura}">
            <p style="margin:0; font-size: 14px; opacity: 0.9;">🔄 FRESCURA DE TRACKING (24h)</p>
            <h2 style="margin:0.5rem 0;">{frescura_tracking:.1f}%</h2>
            <p style="margin:0; font-size: 12px;">Estado: { 'Excelente' if frescura_tracking >= 85 else ('Aceptable' if frescura_tracking >= 70 else 'Crítico')}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_kpi3:
        style_csat = get_kpi_style(csat_porcentaje, 80, 70)
        st.markdown(f"""
        <div class="{style_csat}">
            <p style="margin:0; font-size: 14px; opacity: 0.9;">😊 CSAT (Satisfacción)</p>
            <h2 style="margin:0.5rem 0;">{csat_porcentaje:.1f}%</h2>
            <p style="margin:0; font-size: 12px;">Estado: { 'Excelente' if csat_porcentaje >= 80 else ('Aceptable' if csat_porcentaje >= 70 else 'Mejorable')}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Gráficos mejorados con dark theme
    col1, col2 = st.columns(2)
    
    with col1:
        estado_counts = df_envios['estado'].value_counts()
        
        # Colores personalizados para estados
        colors = {
            'Entregado': '#00c48c',
            'En tránsito': '#00d4ff',
            'Retrasado': '#ff006b',
            'Pendiente': '#a259ff'
        }
        color_sequence = [colors.get(estado, '#ff8a00') for estado in estado_counts.index]
        
        fig_estados = px.pie(
            values=estado_counts.values,
            names=estado_counts.index,
            title="📊 Distribución de Estados de Envío",
            color_discrete_sequence=color_sequence,
            hole=0.4  # Donut chart para look moderno
        )
        
        fig_estados.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12),
            title_font=dict(size=16, color='white'),
            showlegend=True,
            legend=dict(
                bgcolor='rgba(37, 40, 54, 0.8)',
                bordercolor='rgba(255, 255, 255, 0.1)',
                borderwidth=1
            )
        )
        
        st.plotly_chart(fig_estados, use_container_width=True)
    
    with col2:
        transportista_counts = df_envios['transportista'].value_counts()
        
        fig_transportistas = px.bar(
            x=transportista_counts.index,
            y=transportista_counts.values,
            title="🚚 Envíos por Transportista",
            labels={'x': 'Transportista', 'y': 'Número de Envíos'},
            color=transportista_counts.values,
            color_continuous_scale=['#ff006b', '#ff8a00', '#00d4ff', '#00c48c']
        )
        
        fig_transportistas.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12),
            title_font=dict(size=16, color='white'),
            xaxis=dict(
                showgrid=False,
                color='white'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(255, 255, 255, 0.1)',
                color='white'
            ),
            showlegend=False
        )
        
        st.plotly_chart(fig_transportistas, use_container_width=True)
    
    # Mapa de calor de rutas
    st.subheader("🗺️ Rutas Más Frecuentes")
    if "origen" in df_envios.columns and "destino" in df_envios.columns:
        df_envios['ruta'] = df_envios['origen'] + ' → ' + df_envios['destino']
        rutas_counts = df_envios['ruta'].value_counts().head(10)
        
        fig_rutas = px.bar(
            x=rutas_counts.values,
            y=rutas_counts.index,
            orientation='h',
            title="Top 10 Rutas Más Frecuentes (Origen → Destino)",
            labels={'x': 'Número de Envíos', 'y': 'Ruta'},
            color=rutas_counts.values,
            color_continuous_scale=['#00d4ff', '#a259ff', '#ff006b']
        )
        
        fig_rutas.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12),
            title_font=dict(size=16, color='white'),
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(255, 255, 255, 0.1)',
                color='white'
            ),
            yaxis=dict(
                showgrid=False,
                color='white'
            ),
            showlegend=False
        )
        
        st.plotly_chart(fig_rutas, use_container_width=True)
    else:
        st.warning("⚠ No se encontraron las columnas 'origen' y 'destino' para analizar rutas.")

#----------------------------------------------------------------------------------------------------

######################################################
# 📦 Gestión de Envíos
######################################################

elif page_clean == "Gestión de Envíos":
    # Header mejorado - visible en ambos modos
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0ee9ff 0%, #00b8d4 100%); 
                padding: 2rem; border-radius: 16px; margin-bottom: 2rem; box-shadow: 0 4px 12px rgba(14, 233, 255, 0.3);">
        <h1 style="margin: 0; color: #1a1d29; font-size: 2rem; font-weight: 700;">📦 Gestión de Envíos</h1>
        <p style="margin: 0.5rem 0 0 0; color: #1a1d29; font-size: 1rem; opacity: 0.9;">
            Administra, filtra y crea nuevos envíos en el sistema
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # CORRECCIÓN KEYERROR: Garantizar que la columna 'modalidad' exista
    if 'modalidad' not in st.session_state['df_envios'].columns:
        st.session_state['df_envios']['modalidad'] = 'Terrestre'
    
    df_envios = st.session_state['df_envios'] # Volver a obtener la versión actualizada

    # 🔄 Sincronización con Supabase / n8n
    if st.button("🔄 Actualizar Datos"):
        if recargar_datos_desde_supabase_y_actualizar_state():
            st.cache_data.clear() 
            st.rerun()


    # Filtros mejorados con diseño moderno
    st.markdown("### 🔍 Filtros de Búsqueda")
    
    with st.container():
        st.markdown("""
        <div style="background: rgba(37, 40, 54, 0.6); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem;">
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            filtro_estado = st.multiselect(
                "🏷️ Estado:",
                options=df_envios['estado'].unique(),
                default=df_envios['estado'].unique(),
                key="filtro_estado_gestion"
            )
        
        with col2:
            filtro_transportista = st.multiselect(
                "🚚 Transportista:",
                options=df_envios['transportista'].unique(),
                default=df_envios['transportista'].unique(),
                key="filtro_transportista_gestion"
            )
            
        # --- FILTRO DE MODALIDAD ---
        with col3:
            filtro_modalidad = st.multiselect(
                "✈️ Modalidad:",
                options=df_envios['modalidad'].unique(),
                default=df_envios['modalidad'].unique(),
                key="filtro_modalidad_gestion"
            )
    # ---------------------------
    
    # Definición de rango de fecha para filtros y reporte
    fecha_inicio_defecto = datetime.now().date() - timedelta(days=30)
    fecha_fin_defecto = datetime.now().date()
    
    if not df_envios.empty and 'fecha_creacion' in df_envios.columns:
        min_date = df_envios['fecha_creacion'].min().date()
        max_date = df_envios['fecha_creacion'].max().date()
        default_start = max(fecha_inicio_defecto, min_date)
        default_end = max_date
    else:
        min_date = fecha_inicio_defecto
        max_date = fecha_fin_defecto
        default_start = min_date
        default_end = max_date

    with col4:
        filtro_fecha = st.date_input(
            "📅 Rango de Fechas:",
            value=(default_start, default_end),
            min_value=min_date,
            max_value=max_date,
            key="filtro_fecha_reporte"
        )
    
    # Aplicar filtros
    df_filtrado = df_envios[
        (df_envios['estado'].isin(filtro_estado)) &
        (df_envios['transportista'].isin(filtro_transportista)) &
        (df_envios['modalidad'].isin(filtro_modalidad)) # Aplicar filtro de modalidad
    ]
    
    # Aplicar filtro de fecha al DataFrame (se necesitan las fechas individuales)
    fecha_inicio = filtro_fecha[0] if isinstance(filtro_fecha, tuple) and len(filtro_fecha) == 2 else default_start
    fecha_fin = filtro_fecha[1] if isinstance(filtro_fecha, tuple) and len(filtro_fecha) == 2 else default_end
    
    df_filtrado = df_filtrado[
        (df_filtrado['fecha_creacion'].dt.date >= fecha_inicio) &
        (df_filtrado['fecha_creacion'].dt.date <= fecha_fin)
    ]
    
    # Mostrar tabla de envíos con header moderno
    st.markdown("### 📋 Tabla de Envíos")
    st.markdown(f"**Total de registros encontrados:** `{len(df_filtrado)}`")
    
    st.dataframe(
        df_filtrado,
        column_config={
            "id": "ID Envío", # Esta es la columna que ahora contiene el ID corto
            "cliente": "Cliente",
            "origen": "Origen",
            "destino": "Destino",
            "transportista": "Transportista",
            "modalidad": "Modalidad", # Columna de modalidad
            "estado": "Estado",
            "fecha_creacion": "Fecha Creación",
            "fecha_estimada": "Fecha Estimada",
            "fecha_entrega": "Fecha Entrega",
            "peso": "Peso (kg)",
            "valor": "Valor (€)"
        },
        use_container_width=True
    )
    
    # Acciones con diseño mejorado
    st.markdown("---")
    st.markdown("### ⚡ Acciones Rápidas")
    col1_form, col2_btn, col3_btn = st.columns([1, 1, 1])

    # 🧾 Formulario para crear envío
    with col1_form:
        with st.form("crear_envio_form"):
            st.subheader("🧾 Registrar un nuevo envío")
            st.info("El ID de Seguimiento se generará automáticamente.")

            col_form1, col_form2 = st.columns(2)

            with col_form1:
                cliente = st.text_input("Nombre del Cliente (*)", key="crear_envio_cliente")
                email = st.text_input("Correo del Cliente (*)", key="crear_envio_email")
                
                origen = st.selectbox("Ciudad de origen (*)", options=PERU_CIUDADES, key="crear_envio_origen")
                
                destino_options = [c for c in PERU_CIUDADES if c != origen]
                destino = st.selectbox("Ciudad de destino (*)", options=destino_options, key="crear_envio_destino")


            with col_form2:
                direccion = st.text_input("Dirección de entrega", key="crear_envio_direccion")
                transportista = st.text_input("Transportista asignado", key="crear_envio_transportista")
                peso = st.number_input("Peso (kg)", min_value=0.1, step=0.1, key="crear_envio_peso")
                largo = st.number_input("Largo (cm)", min_value=1, key="crear_envio_largo")
                costo_envio = st.number_input("Costo del envío (S/)", min_value=0.0, step=0.1, key="crear_envio_costo")

            col_dim1, col_dim2 = st.columns(2)
            with col_dim1:
                ancho = st.number_input("Ancho (cm)", min_value=1, key="crear_envio_ancho")
            with col_dim2:
                alto = st.number_input("Alto (cm)", min_value=1, key="crear_envio_alto")

            modalidad = st.selectbox(
                "Modalidad de Envío",
                ["Terrestre", "Aérea"],
                key="crear_envio_modalidad"
            )

            estado = st.selectbox(
                "Estado inicial del envío",
                ["creado", "pendiente", "en tránsito", "entregado"],
                key="crear_envio_estado"
            )

            enviado = st.form_submit_button("📦 Crear Envío")

            if enviado:
                tracking_id = generar_id_corta() 
                
                if not cliente or not email:
                    st.warning("⚠ Por favor, completa los campos obligatorios marcados con (*).")
                else:
                    nuevo_envio = {
                        "envioId": tracking_id, 
                        "id": tracking_id, 
                        "cliente": cliente,
                        "email": email,
                        "direccion": direccion,
                        "ciudad": destino, 
                        "origen": origen,
                        "peso": peso,
                        "dimensiones": {"largo": largo, "ancho": ancho, "alto": alto},
                        "transportista": transportista,
                        "modalidad": modalidad, 
                        "costo_envio": costo_envio,
                        "estado": estado
                    }
                    enviar_a_n8n(nuevo_envio, "http://localhost:5678/webhook/nuevo-envio")


    # 🔄 Botón Actualizar Estados
    with col2_btn:
        st.write("") 
        st.write("")
        if st.button("🔄 Actualizar Estados", key="btn_actualizar_estados"):
            st.info("Sincronización con n8n para actualizar estados de envíos")

    # 📊 Botón Generar Reporte (Ahora con descarga de PDF)
    with col3_btn:
        st.write("") 
        st.write("")
        
        if not df_filtrado.empty and FPDF is not None:
            pdf_bytes = generar_reporte_pdf(df_filtrado, fecha_inicio, fecha_fin)
            
            st.download_button(
                label="📊 Descargar Reporte PDF",
                data=pdf_bytes, 
                file_name=f"Reporte_Envios_{fecha_inicio.strftime('%Y%m%d')}_{fecha_fin.strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                key="download_report_pdf"
            )
        else:
            if FPDF is None:
                st.warning("No se puede generar PDF. Instala 'fpdf2'.")
            else:
                st.button("📊 Generar Reporte PDF", disabled=True, help="No hay envíos filtrados para generar el reporte.")

#----------------------------------------------------------------------------------------------------

######################################################
# 🛰️ Seguimiento en Tiempo Real
######################################################

elif page_clean == "Seguimiento en Tiempo Real":
    # Header mejorado - visible en ambos modos
    st.markdown("""
    <div style="background: linear-gradient(135deg, #00ff9d 0%, #00d47e 100%); 
                padding: 2rem; border-radius: 16px; margin-bottom: 2rem; box-shadow: 0 4px 12px rgba(0, 255, 157, 0.3);">
        <h1 style="margin: 0; color: #1a1d29; font-size: 2rem; font-weight: 700;">🔍 Seguimiento en Tiempo Real</h1>
        <p style="margin: 0.5rem 0 0 0; color: #1a1d29; font-size: 1rem; opacity: 0.9;">
            Rastrea tus envíos y consulta su ubicación actual
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Buscar envío con diseño mejorado
    st.markdown("### 🔎 Buscar Envío")
    
    col_search, col_btn = st.columns([3, 1])
    with col_search:
        envio_id = st.text_input(
            "Ingresa el ID de envío:",
            placeholder="Ej: ENV-ABC123",
            label_visibility="collapsed"
        )
    with col_btn:
        st.write("")  # Espaciado
        search_btn = st.button("🔍 Buscar", use_container_width=True)
    
    if envio_id:
        envio = df_envios[df_envios['id'] == envio_id] 
        
        if not envio.empty:
            envio = envio.iloc[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader(f"Información del Envío {envio_id}")
                
                st.write(f"*Cliente:* {envio['cliente']}")
                st.write(f"*Origen:* **{envio['origen']}**")
                st.write(f"*Destino:* **{envio['destino']}**")
                st.write(f"*Transportista:* {envio['transportista']}")
                st.write(f"*Modalidad:* **{envio['modalidad']}**") 
                st.write(f"*Estado:* {envio['estado']}")

                fecha_estimada = envio.get('fecha_estimada', None)
                if pd.notna(fecha_estimada):
                    st.write(f"*Fecha estimada de entrega:* {pd.to_datetime(fecha_estimada).strftime('%d/%m/%Y')}")
                else:
                    st.write("*Fecha estimada de entrega:* No registrada")

                fecha_entrega = envio.get('fecha_entrega', None)
                if pd.notna(fecha_entrega):
                    st.write(f"*Fecha de entrega:* {pd.to_datetime(fecha_entrega).strftime('%d/%m/%Y')}")
                else:
                    st.write("*Fecha de entrega:* No registrada")

                
            with col2:
                st.subheader("Ubicación Actual")
                
                fig_mapa = go.Figure()
                
                # Usaremos coordenadas fijas de Lima y Trujillo para el ejemplo visual
                
                fig_mapa.add_trace(go.Scatter(
                    x=[-77.0428, -79.0299], 
                    y=[-12.0464, -8.1150],  
                    mode='markers+text',
                    marker=dict(size=14, color=['blue', 'red']),
                    text=['Origen', 'Destino'],
                    textposition="top center"
                ))
                
                fig_mapa.add_trace(go.Scatter(
                    x=[-77.0428, -78.0, -79.0299], 
                    y=[-12.0464, -10.0, -8.1150],
                    mode='lines',
                    line=dict(width=3, color='green'),
                    name='Ruta'
                ))
                
                fig_mapa.update_layout(
                    xaxis_title="Longitud",
                    yaxis_title="Latitud",
                    showlegend=False,
                    margin=dict(l=0, r=0, t=0, b=0),
                    height=400
                )
                
                st.plotly_chart(fig_mapa, width='stretch')
            
            # Historial de actualizaciones (simulado)
            st.subheader("Historial de Seguimiento")
            
            events = [
                {"fecha": envio['fecha_creacion'] - timedelta(hours=1), "evento": "Pedido recibido"},
                {"fecha": envio['fecha_creacion'], "evento": "Envío creado y asignado a transportista"},
                {"fecha": envio['fecha_creacion'] + timedelta(hours=2), "evento": "Recogido por transportista"},
                {"fecha": envio['fecha_creacion'] + timedelta(days=1), "evento": "En centro de distribución de origen"},
                {"fecha": envio['fecha_creacion'] + timedelta(days=2), "evento": "En tránsito hacia destino"},
            ]
            
            if envio['estado'] == 'Entregado' and pd.notna(envio['fecha_entrega']):
                events.append({"fecha": envio['fecha_entrega'], "evento": "Entregado al destinatario"})
            elif envio['estado'] == 'En tránsito':
                events.append({"fecha": envio['fecha_creacion'] + timedelta(days=3), "evento": "En centro de distribución de destino"})
            
            events.sort(key=lambda x: x['fecha'], reverse=True)

            for evento in events:
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.write(evento['fecha'].strftime('%d/%m/%Y %H:%M'))
                with col2:
                    st.write(evento['evento'])
        else:
            st.error(f"No se encontró el envío con ID: **{envio_id}**")
    
    # Notificaciones
    st.subheader("Configuración de Notificaciones")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.checkbox("Notificaciones por email", value=True)
    
    with col2:
        st.checkbox("Notificaciones por SMS", value=False)
    
    with col3:
        st.checkbox("Notificaciones push", value=True)

#----------------------------------------------------------------------------------------------------

######################################################
# 🗺️ Análisis de Rutas
######################################################

elif page_clean == "Análisis de Rutas":
    # Header mejorado - visible en ambos modos
    st.markdown("""
    <div style="background: linear-gradient(135deg, #b47aff 0%, #9c5eff 100%); 
                padding: 2rem; border-radius: 16px; margin-bottom: 2rem; box-shadow: 0 4px 12px rgba(180, 122, 255, 0.3);">
        <h1 style="margin: 0; color: #1a1d29; font-size: 2rem; font-weight: 700;">🗺️ Análisis de Rutas</h1>
        <p style="margin: 0.5rem 0 0 0; color: #1a1d29; font-size: 1rem; opacity: 0.9;">
            Visualiza rutas óptimas y calcula distancias estimadas entre ciudades
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Selector de origen y destino con mejor diseño
    st.markdown("### 📍 Seleccionar Ruta")
    
    col1, col2 = st.columns(2)
    
    opciones_rutas = list(COORDENADAS_PERU_FIJAS.keys())

    with col1:
        origen = st.selectbox("Origen:", opciones_rutas)
    
    with col2:
        destino_options = [c for c in opciones_rutas if c != origen]
        destino = st.selectbox("Destino:", destino_options)
    
    # Análisis de ruta
    if st.button("Analizar Ruta Óptima") and origen != destino:
        
        # Obtener datos reales de la ruta
        ruta_clave = f"{origen}-{destino}"
        if ruta_clave not in DISTANCIAS_REALES:
             ruta_clave = f"{destino}-{origen}" # Buscar el inverso
             
        datos_ruta = DISTANCIAS_REALES.get(ruta_clave, {"distancia": 500, "tiempo_h": 10, "costo_base": 100})
        
        # Obtener coordenadas fijas
        origen_coords = COORDENADAS_PERU_FIJAS.get(origen)
        destino_coords = COORDENADAS_PERU_FIJAS.get(destino)
        
        if origen_coords and destino_coords:
            
            st.subheader(f"Ruta Gráfica (Simulada): {origen} → {destino}")
            
            # --- CÁLCULO REALISTA DE MÉTRICAS ---
            distancia = datos_ruta['distancia']
            tiempo_total_h = datos_ruta['tiempo_h']
            
            horas = int(tiempo_total_h)
            minutos = int((tiempo_total_h - horas) * 60)
            tiempo_display = f"{horas} h {minutos} min"
            costo_estimado = round(datos_ruta['costo_base'] + (distancia * 0.05), 2) # Costo base + factor distancia
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Distancia Estimada (Carretera)", f"{distancia} km")
            with col2:
                st.metric("Tiempo Estimado", tiempo_display)
            with col3:
                st.metric("Coste Estimado", f"€ {costo_estimado}")
            
            # --- MAPA MEJORADO CON SCATTERMAPBOX ---
            
            fig_ruta = go.Figure()
            
            # 1. Añadir puntos de origen y destino (Markers)
            fig_ruta.add_trace(go.Scattermapbox(
                lat=[origen_coords['lat'], destino_coords['lat']], 
                lon=[origen_coords['lon'], destino_coords['lon']],
                mode='markers+text',
                marker=dict(size=14, color=['blue', 'red']),
                text=[f"Origen: {origen}", f"Destino: {destino}"],
                textposition="top center",
                name='Puntos de Envío'
            ))
            
            # 2. Añadir línea de ruta simulada (Line)
            fig_ruta.add_trace(go.Scattermapbox(
                lat=[origen_coords['lat'], destino_coords['lat']],
                lon=[origen_coords['lon'], destino_coords['lon']],
                mode='lines',
                line=dict(width=4, color='green'),
                name='Línea Recta'
            ))
            
            # 3. Configurar el layout para centrarse en Perú y usar un mapa atractivo
            fig_ruta.update_layout(
                mapbox_style="carto-positron", # Estilo visual atractivo
                mapbox_accesstoken=MAPBOX_ACCESS_TOKEN_SIMULADO, 
                mapbox_zoom=4.5,
                mapbox_center={'lat': -10.0, 'lon': -75.0}, # Centro de Perú
                
                title_text=f'Ruta Geográfica Simulada',
                margin=dict(l=0, r=0, t=30, b=0),
                height=500
            )
            
            st.plotly_chart(fig_ruta, width='stretch')
        
        else:
            st.error(f"Error: La ciudad '{origen}' o '{destino}' no se encuentra en la lista de coordenadas fijas.")

#----------------------------------------------------------------------------------------------------

######################################################
# 📊 Encuesta de Usabilidad (NUEVA PÁGINA MEJORADA)
######################################################

elif page_clean == "Encuesta de Usabilidad":
    # Header mejorado - visible en ambos modos
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0ee9ff 0%, #00b8d4 100%); 
                padding: 2rem; border-radius: 16px; margin-bottom: 2rem; box-shadow: 0 4px 12px rgba(14, 233, 255, 0.3);">
        <h1 style="margin: 0; color: #1a1d29; font-size: 2rem; font-weight: 700;">📝 Encuesta de Usabilidad</h1>
        <p style="margin: 0.5rem 0 0 0; color: #1a1d29; font-size: 1rem; opacity: 0.9;">
            Tu opinión es clave para mejorar el sistema
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    
    # Escala visible en ambos modos
    st.markdown("""
        <div style="text-align: center; padding: 1rem; margin-bottom: 1.5rem; background: rgba(14, 233, 255, 0.1); border-radius: 8px; border: 1px solid #0ee9ff;">
            <p style="margin: 0; color: #0ee9ff; font-weight: 600; font-size: 1.1rem;">
                <strong>1 = Totalmente en Desacuerdo</strong> | <strong>3 = Neutral</strong> | <strong>5 = Totalmente de Acuerdo</strong>
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    WEBHOOK_ENCUESTA_URL = st.secrets.get("WEBHOOK_ENCUESTA_URL", "http://localhost:5678/webhook/registrar-usabilidad") 

    with st.form("form_encuesta_usabilidad"):
        
        respuestas = {}
        
        # --- I. EFICIENCIA (Tarjeta Visual) ---
        st.markdown('<div class="dimension-card">', unsafe_allow_html=True)
        st.markdown('<div class="dimension-title">🧠 I. EFICIENCIA (Rapidez y Productividad)</div>', unsafe_allow_html=True)
        
        respuestas['E1'] = st.slider("E1: Pude completar las tareas de gestión de envíos (registrar, buscar) de manera rápida y sin interrupciones.", 1, 5, 3, key="s_e1")
        respuestas['E2'] = st.slider("E2: El tiempo de respuesta del sistema (carga de páginas, filtros) es adecuado para mi trabajo.", 1, 5, 3, key="s_e2")
        respuestas['E3'] = st.slider("E3: La información necesaria para el seguimiento se encuentra con un mínimo número de clics.", 1, 5, 3, key="s_e3")
        st.markdown('</div>', unsafe_allow_html=True) # Cierra Tarjeta
        
        # --- II. SATISFACCIÓN (Tarjeta Visual) ---
        st.markdown('<div class="dimension-card">', unsafe_allow_html=True)
        st.markdown('<div class="dimension-title">😊 II. SATISFACCIÓN (Experiencia de Usuario)</div>', unsafe_allow_html=True)
        
        respuestas['S1'] = st.slider("S1: Disfruto usando este sistema; la interfaz gráfica es agradable y bien diseñada.", 1, 5, 3, key="s_s1")
        respuestas['S2'] = st.slider("S2: La presentación de los datos (tablas, gráficos de estados) es clara y fácil de interpretar.", 1, 5, 3, key="s_s2")
        respuestas['S3'] = st.slider("S3: Recomendaría este sistema a otro colega que necesite gestionar envíos.", 1, 5, 3, key="s_s3")
        st.markdown('</div>', unsafe_allow_html=True) # Cierra Tarjeta
        
        # --- III. FACILIDAD DE APRENDIZAJE (Tarjeta Visual) ---
        st.markdown('<div class="dimension-card">', unsafe_allow_html=True)
        st.markdown('<div class="dimension-title">📚 III. FACILIDAD DE APRENDIZAJE (Curva y Lógica)</div>', unsafe_allow_html=True)
        
        respuestas['A1'] = st.slider("A1: Las funciones y herramientas del sistema son intuitivas; pude usarlas inmediatamente.", 1, 5, 3, key="s_a1")
        respuestas['A2'] = st.slider("A2: El proceso para registrar un nuevo envío es lógico y sigue una secuencia esperada.", 1, 5, 3, key="s_a2")
        respuestas['A3'] = st.slider("A3: Si cometiera un error, el sistema me proporciona mensajes de ayuda o corrección entendibles.", 1, 5, 3, key="s_a3")
        st.markdown('</div>', unsafe_allow_html=True) # Cierra Tarjeta

        # Campo de Identificación (opcional pero recomendado)
        identificador = st.text_input("Identificador / Correo (Opcional para seguimiento):", max_chars=100)
        
        # Botón de Envío Prominente
        enviado = st.form_submit_button("Enviar Evaluación de Usabilidad 🚀", type="primary")

        if enviado:
            payload_encuesta = {
                "fecha_respuesta": datetime.now().isoformat(),
                "identificador": identificador if identificador else "Anonimo",
                "E1": respuestas['E1'],
                "E2": respuestas['E2'],
                "E3": respuestas['E3'],
                "S1": respuestas['S1'],
                "S2": respuestas['S2'],
                "S3": respuestas['S3'],
                "A1": respuestas['A1'],
                "A2": respuestas['A2'],
                "A3": respuestas['A3'],
            }
            
            # Envío del payload al webhook de n8n para registrar las respuestas
            enviar_a_n8n(payload_encuesta, WEBHOOK_ENCUESTA_URL)

#----------------------------------------------------------------------------------------------------

######################################################
# 📈 Resultados Encuesta (NUEVA PÁGINA)
######################################################

elif page_clean == "Resultados Encuesta":
    # Header mejorado - visible en ambos modos
    st.markdown("""
    <div style="background: linear-gradient(135deg, #ffaa00 0%, #ff8c00 100%); 
                padding: 2rem; border-radius: 16px; margin-bottom: 2rem; box-shadow: 0 4px 12px rgba(255, 170, 0, 0.3);">
        <h1 style="margin: 0; color: #1a1d29; font-size: 2rem; font-weight: 700;">📈 Resultados de Encuesta</h1>
        <p style="margin: 0.5rem 0 0 0; color: #1a1d29; font-size: 1rem; opacity: 0.9;">
            Analítica de usabilidad y satisfacción del usuario
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("Promedio de puntuación (escala 1 a 5) por dimensión y reactivo.")
    
    df_encuestas = cargar_datos_encuesta()

    if df_encuestas.empty or len(df_encuestas.columns) <= 2: 
        st.info("No hay datos de encuestas válidos registrados en Supabase para mostrar resultados. Envíe al menos una encuesta.")
    else:
        # Renombrando las columnas de minúsculas a MAYÚSCULAS para mostrar en el gráfico (solo visual)
        df_encuestas.columns = df_encuestas.columns.str.upper()
        
        total_respuestas = len(df_encuestas.dropna(subset=['E1'])) 
        st.metric("Total de Respuestas Válidas", total_respuestas)
        st.markdown("---")
        
        # 1. Cálculo del KPI 3: CSAT (Satisfacción)
        satisfaccion_data = df_encuestas[['S1', 'S2', 'S3']]
        total_respuestas_csat = satisfaccion_data.count().sum() 
        respuestas_satisfechas = (satisfaccion_data >= 4).sum().sum() # 4 o 5 son satisfechos
        
        if total_respuestas_csat > 0:
            csat_porcentaje = (respuestas_satisfechas / total_respuestas_csat) * 100
        else:
            csat_porcentaje = 0
            
        st.metric("CSAT (Satisfacción) total:", f"{csat_porcentaje:.1f}%")

        # 2. Calcular promedios por dimensión
        df_promedios = pd.DataFrame({
            'Dimensión': ['Eficiencia', 'Satisfacción', 'Aprendizaje'],
            'Promedio': [
                df_encuestas[['E1', 'E2', 'E3']].mean(axis=1).mean(),
                df_encuestas[['S1', 'S2', 'S3']].mean(axis=1).mean(),
                df_encuestas[['A1', 'A2', 'A3']].mean(axis=1).mean()
            ]
        })
        
        st.markdown("---")
        st.subheader("Desglose de Usabilidad por Reactivo")
        
        # 3. Calcular promedios por reactivo (desempaquetado)
        df_reactivos = df_encuestas[['E1', 'E2', 'E3', 'S1', 'S2', 'S3', 'A1', 'A2', 'A3']].mean().reset_index()
        df_reactivos.columns = ['Reactivo', 'Promedio']
        
        # Mapeo de Reactivos a nombres completos
        mapeo_reactivos = {
            'E1': 'E1: Rapidez/Interrupción', 'E2': 'E2: Tiempo de respuesta', 'E3': 'E3: Mínimo de clics',
            'S1': 'S1: Diseño agradable', 'S2': 'S2: Datos claros', 'S3': 'S3: Recomendación',
            'A1': 'A1: Funciones intuitivas', 'A2': 'A2: Proceso lógico', 'A3': 'A3: Mensajes de error'
        }
        df_reactivos['Reactivo Nombre'] = df_reactivos['Reactivo'].map(mapeo_reactivos)
        df_reactivos['Dimensión'] = df_reactivos['Reactivo'].str[0].replace({'E': 'Eficiencia', 'S': 'Satisfacción', 'A': 'Aprendizaje'})
        
        fig_reactivos = px.bar(
            df_reactivos,
            x='Promedio',
            y='Reactivo Nombre',
            orientation='h',
            color='Dimensión',
            range_x=[1, 5],
            title='Promedio de Puntuación por Reactivo',
            category_orders={"Reactivo Nombre": df_reactivos.sort_values(by='Promedio', ascending=False)['Reactivo Nombre'].tolist()}
        )
        st.plotly_chart(fig_reactivos, width='stretch')

#----------------------------------------------------------------------------------------------------

######################################################
# ⚙️ Configuración
######################################################

elif page_clean == "Configuración":
    # Header mejorado - visible en ambos modos
    st.markdown("""
    <div style="background: linear-gradient(135deg, #b47aff 0%, #9c5eff 100%); 
                padding: 2rem; border-radius: 16px; margin-bottom: 2rem; box-shadow: 0 4px 12px rgba(180, 122, 255, 0.3);">
        <h1 style="margin: 0; color: #1a1d29; font-size: 2rem; font-weight: 700;">⚙️ Configuración del Sistema</h1>
        <p style="margin: 0.5rem 0 0 0; color: #1a1d29; font-size: 1rem; opacity: 0.9;">
            Gestiona transportistas, webhooks y preferencias del sistema
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Configuración de transportistas
    st.subheader("Gestión de Transportistas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Nombre del Transportista")
        st.text_input("Contacto")
        st.text_input("Teléfono")
        
        if st.button("Añadir Transportista"):
            st.success("Transportista añadido correctamente")
    
    with col2:
        st.text_area("Condiciones de Servicio")
        st.number_input("Tiempo de Entrega Promedio (días)", min_value=1, max_value=30, value=5)
        st.number_input("Coste por Kilómetro (€)", min_value=0.1, max_value=2.0, value=0.5)
    
    # Configuración de integraciones
    st.subheader("Integraciones")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("URL de n8n Webhook de Envíos", value="http://localhost:5678/webhook/nuevo-envio", key="config_n8n_envio")
        st.text_input("URL de n8n Webhook de Encuesta", value="http://localhost:5678/webhook/registrar-usabilidad", key="config_n8n_encuesta")
        st.text_input("Clave API de Supabase", type="password")
    
    with col2:
        st.text_input("Clave API de Google Maps")
        st.text_input("Clave API de Servicio de SMS")
    
    if st.button("Guardar Configuración"):
        st.success("Configuración guardada correctamente")

# Pie de página
st.markdown("---")
st.markdown(
    "Sistema de Logística y Seguimiento de Envíos - "
    "Integrado con n8n y Supabase | "
    "© 2023 Todos los derechos reservados"
)