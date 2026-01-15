# 🚚 Sistema de Logística y Seguimiento de Envíos

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-latest-red.svg)
![Supabase](https://img.shields.io/badge/database-supabase-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

Sistema integral de gestión logística desarrollado con Streamlit para el seguimiento y administración de envíos en tiempo real. Incluye dashboard interactivo, análisis de rutas, gestión de envíos, y sistema de encuestas de usabilidad.

## 📑 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [Módulos del Sistema](#-módulos-del-sistema)
- [Pruebas de Rendimiento](#-pruebas-de-rendimiento)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [API y Webhooks](#-api-y-webhooks)
- [Contribuciones](#-contribuciones)
- [Licencia](#-licencia)

## ✨ Características

### Funcionalidades Principales

- **📊 Dashboard Interactivo**: Visualización en tiempo real de métricas clave (KPIs)
  - Total de envíos y estados
  - Throughput de entregas
  - Frescura de tracking
  - CSAT (Customer Satisfaction Score)
  - Gráficos dinámicos con Plotly

- **📦 Gestión Completa de Envíos**
  - Registro de nuevos envíos con validación
  - Actualización de estados en tiempo real
  - Generación automática de IDs de tracking
  - Cálculo de costos y tiempos estimados
  - Exportación de reportes en PDF

- **🔍 Seguimiento en Tiempo Real**
  - Búsqueda por ID de tracking
  - Historial completo de estados
  - Información detallada del envío
  - Estimaciones de entrega

- **🗺️ Análisis de Rutas**
  - Visualización de rutas en mapa interactivo
  - Cálculo de distancias reales entre ciudades peruanas
  - Optimización de costos de transporte
  - Análisis de tiempos de tránsito

- **📝 Sistema de Encuestas**
  - Encuestas de usabilidad basadas en SUS (System Usability Scale)
  - Análisis de satisfacción del cliente
  - Visualización de resultados por dimensiones
  - Almacenamiento en base de datos

- **⚙️ Configuración Flexible**
  - Gestión de transportistas
  - Configuración de ciudades y rutas
  - Parámetros del sistema personalizables

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐
│   Streamlit UI  │ ← Interfaz de usuario web
└────────┬────────┘
         │
         ├─────────────────┐
         │                 │
    ┌────▼────┐      ┌────▼────┐
    │ Supabase│      │   n8n   │
    │   DB    │      │ Webhook │
    └─────────┘      └─────────┘
         │                 │
         └────────┬────────┘
                  │
         ┌────────▼────────┐
         │  JMeter Tests   │ ← Pruebas de rendimiento
         └─────────────────┘
```

### Tecnologías Utilizadas

- **Frontend**: Streamlit (Python)
- **Base de Datos**: Supabase (PostgreSQL)
- **Visualización**: Plotly, Plotly Express
- **Generación de PDFs**: fpdf2
- **Automatización**: n8n (webhooks)
- **Pruebas de Carga**: Apache JMeter
- **Análisis de Datos**: Pandas, NumPy

## 📋 Requisitos

### Software Necesario

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Cuenta de Supabase (gratuita)
- Apache JMeter (opcional, para pruebas de rendimiento)

### Dependencias de Python

```
streamlit
pandas
plotly
supabase
fpdf2
requests
```

## 🔧 Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/Sosan10/sistema-logistica-envios.git
cd sistema-logistica-envios
```

### 2. Crear Entorno Virtual

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install streamlit pandas plotly supabase fpdf2 requests
```

O si existe un archivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

## ⚙️ Configuración

### 1. Configurar Supabase

1. Crea una cuenta en [Supabase](https://supabase.com)
2. Crea un nuevo proyecto
3. Ejecuta el siguiente SQL para crear las tablas necesarias:

```sql
-- Tabla de envíos
CREATE TABLE envios (
    id SERIAL PRIMARY KEY,
    envioId VARCHAR(20) UNIQUE NOT NULL,
    cliente VARCHAR(100),
    origen VARCHAR(50),
    destino VARCHAR(50),
    transportista VARCHAR(100),
    estado VARCHAR(20),
    fecha_creacion TIMESTAMP DEFAULT NOW(),
    fecha_estimada TIMESTAMP,
    fecha_entrega TIMESTAMP,
    peso DECIMAL(10,2),
    valor DECIMAL(10,2),
    etiqueta VARCHAR(50),
    modalidad VARCHAR(20),
    ultima_actualizacion TIMESTAMP DEFAULT NOW()
);

-- Tabla de encuestas
CREATE TABLE encuesta_usabilidad (
    id SERIAL PRIMARY KEY,
    identificador VARCHAR(100),
    fecha_respuesta TIMESTAMP DEFAULT NOW(),
    e1 INTEGER,
    e2 INTEGER,
    e3 INTEGER,
    s1 INTEGER,
    s2 INTEGER,
    s3 INTEGER,
    a1 INTEGER,
    a2 INTEGER,
    a3 INTEGER
);
```

### 2. Configurar Secrets de Streamlit

Crea el archivo `.streamlit/secrets.toml` en el directorio del proyecto:

```toml
SUPABASE_URL = "tu-url-de-supabase"
SUPABASE_KEY = "tu-clave-anon-de-supabase"
```

> ⚠️ **IMPORTANTE**: Este archivo contiene información sensible y NO debe subirse a GitHub. Ya está incluido en `.gitignore`.

### 3. Configurar n8n (Opcional)

Si deseas usar webhooks de n8n para automatización:

1. Instala y configura [n8n](https://n8n.io)
2. Importa el flujo desde `flujo_logistica_n8n.json`
3. Actualiza las URLs de webhook en el código si es necesario

## 🏃 Uso

### Iniciar la Aplicación

```bash
streamlit run logistica_envios/app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

### Poblar la Base de Datos (Primera Vez)

```bash
python populate_database.py
```

Este script creará datos de ejemplo en tu base de datos de Supabase.

## 📱 Módulos del Sistema

### 1. Dashboard (📊)
- Visualización de métricas clave
- Gráficos de distribución de envíos
- KPIs de rendimiento
- Análisis de estados

### 2. Gestión de Envíos (📦)
- **Registrar Nuevo Envío**: Formulario completo con validación
- **Actualizar Estado**: Cambio de estado de envíos existentes
- **Generar Reportes**: Exportación a PDF con filtros por fecha

### 3. Seguimiento en Tiempo Real (🔍)
- Búsqueda por ID de tracking
- Visualización de información completa
- Historial de estados
- Estimaciones de entrega

### 4. Análisis de Rutas (🗺️)
- Mapa interactivo de Perú
- Rutas entre Lima, Trujillo y Arequipa
- Cálculo de distancias y costos
- Visualización de tráfico de envíos

### 5. Encuesta de Usabilidad (📝)
- Basada en System Usability Scale (SUS)
- 9 preguntas en 3 dimensiones:
  - Eficiencia
  - Satisfacción
  - Aprendizaje
- Almacenamiento automático en BD

### 6. Resultados de Encuesta (📈)
- Análisis estadístico de respuestas
- Gráficos por dimensión
- Promedios y distribuciones
- Exportación de datos

### 7. Configuración (⚙️)
- Gestión de transportistas
- Configuración de ciudades
- Parámetros del sistema

## 📊 Pruebas de Rendimiento

El proyecto incluye configuraciones de JMeter para pruebas de carga:

### Archivos de Configuración

- `jmeter/SistemaGlobal.jmx`: Pruebas del sistema completo
- `jmeter/Sistema_PorNivel.jmx`: Pruebas por niveles de concurrencia
- `Reporte resumen.jmx`: Generación de reportes

### Ejecutar Pruebas

```bash
# Generar configuración JMX por nivel
python jmeter/generar_jmx_por_nivel.py

# Ejecutar con JMeter (requiere instalación de JMeter)
jmeter -n -t jmeter/SistemaGlobal.jmx -l resultados.jtl
```

### Generar Métricas

```bash
python generar_tabla_metricas.py
```

Esto generará:
- `jmeter/tabla_metricas_rendimiento.csv`
- `jmeter/tabla_metricas_rendimiento.md`

Ver `jmeter/INSTRUCCIONES.md` para más detalles.

## 📁 Estructura del Proyecto

```
sistema-logistica-envios/
├── .streamlit/
│   └── secrets.toml          # Configuración de Supabase (NO subir a Git)
├── logistica_envios/
│   └── app.py                # Aplicación principal de Streamlit
├── jmeter/
│   ├── SistemaGlobal.jmx     # Configuración JMeter global
│   ├── Sistema_PorNivel.jmx  # Configuración JMeter por nivel
│   ├── generar_jmx_por_nivel.py  # Generador de archivos JMX
│   ├── INSTRUCCIONES.md      # Guía de pruebas JMeter
│   ├── tabla_metricas_rendimiento.csv  # Resultados
│   └── tabla_metricas_rendimiento.md   # Resultados formateados
├── populate_database.py      # Script para poblar BD
├── generar_tabla_metricas.py # Generador de métricas
├── check_schema.py           # Verificador de esquema BD
├── fix_estados.py            # Corrector de estados
├── test_supabase.py          # Pruebas de conexión
├── test_fpdf_import.py       # Pruebas de PDF
├── flujo_logistica_n8n.json  # Flujo de n8n
├── .gitignore                # Archivos ignorados por Git
└── README.md                 # Este archivo
```

## 🔌 API y Webhooks

### Supabase API

El sistema utiliza la API REST de Supabase para:
- Consultar envíos: `supabase.table("envios").select("*")`
- Insertar envíos: `supabase.table("envios").insert(data)`
- Actualizar envíos: `supabase.table("envios").update(data).eq("id", id)`

### Webhooks n8n

Endpoints configurables para:
- Registro de nuevos envíos
- Actualización de estados
- Envío de encuestas

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para contribuir:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Guías de Contribución

- Sigue las convenciones de código PEP 8 para Python
- Documenta nuevas funcionalidades
- Agrega pruebas cuando sea posible
- Actualiza el README si es necesario

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👤 Autor

**Yoel Armando Solorzano Sanchez**
- Email: ysolorzano@unitru.edu.pe
- GitHub: [@Sosan10](https://github.com/Sosan10)

## 🙏 Agradecimientos

- Streamlit por el framework de desarrollo
- Supabase por la infraestructura de base de datos
- La comunidad de Python por las excelentes librerías

## 📞 Soporte

Si encuentras algún problema o tienes preguntas:

1. Revisa la [documentación](#)
2. Busca en [Issues existentes](https://github.com/Sosan10/sistema-logistica-envios/issues)
3. Crea un [nuevo Issue](https://github.com/Sosan10/sistema-logistica-envios/issues/new)

---

**⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub!**
