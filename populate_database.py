from supabase import create_client
import random
import string

SUPABASE_URL = "https://fxvbdigahsnfsnikxrxf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ4dmJkaWdhaHNuZnNuaWt4cnhmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIyODMyODgsImV4cCI6MjA3Nzg1OTI4OH0.ZtAwl8CmqY5yXnjWNWR0j6zhMpc9CcwnqXp4lOLwIYo"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Datos para Perú
PERU_CIUDADES = ["Lima", "Trujillo", "Arequipa", "Cusco", "Chiclayo", "Piura"]
TRANSPORTISTAS = ["Transporte Rápido SA", "Logística Nacional", "Envía Seguro", "Mensajería Express", "Olva Courier", "Shalom Courier"]
ESTADOS = ["creado", "pendiente", "en tránsito", "entregado"]
MODALIDADES = ["Terrestre", "Aérea"]

# Empresas peruanas ficticias
EMPRESAS = [
    "Compañía Minera del Sur", "Textiles Lima SAC", "Agroindustrias del Norte",
    "Pesquera Pacifico", "Constructora Andina", "Comercial Central", 
    "Farmacéutica San Juan", "Tecnología Digital Perú", "Alimentos del Valle",
    "Distribuidora Nacional"
]

def generar_id_corta(prefix="ENV"):
    caracteres = string.ascii_uppercase + string.digits
    sufijo = ''.join(random.choices(caracteres, k=5))
    return f"{prefix}-{sufijo}"

def generar_envios(cantidad=100):
    """Genera envíos siguiendo EXACTAMENTE el esquema de la tabla"""
    envios = []
    
    for i in range(cantidad):
        tracking_id = generar_id_corta()
        origen = random.choice(PERU_CIUDADES)
        destino = random.choice([c for c in PERU_CIUDADES if c!= origen])
        
        # Estado con distribución realista
        estado = random.choices(
            ESTADOS,
            weights=[10, 15, 30, 45],  # Más entregados
            k=1
        )[0]
        
        envio = {
            # Columnas que SÍ existen en la tabla
            "id": tracking_id,
            "cliente": random.choice(EMPRESAS),
            "email": f"logistica@{random.choice(EMPRESAS).lower().replace(' ', '')[:10]}.com.pe",
            "origen": origen,
            "destino": destino,
            "transportista": random.choice(TRANSPORTISTAS),
            "estado": estado,
            "direccion": f"{random.choice(['Av. Industrial', 'Jr. Comercio', 'Calle Los Andes'])} {random.randint(100, 999)}",
            "ciudad": destino,
            "peso": round(random.uniform(1, 50), 2),
            "largo": random.randint(20, 120),
            "ancho": random.randint(15, 100),
            "alto": random.randint(10, 80),
            "modalidad": random.choice(MODALIDADES),
            "costo_envio": round(random.uniform(80, 1200), 2),
            "envioId": tracking_id
        }
        
        envios.append(envio)
    
    return envios

def generar_encuestas(cantidad=50):
    """Genera encuestas siguiendo el esquema exacto"""
    encuestas = []
    
    for i in range(cantidad):
        # Tendencia positiva (3-5)
        base = random.randint(3, 5)
        
        encuesta = {
            # Eficiencia
            "e1": min(5, max(1, base + random.randint(-1, 1))),
            "e2": min(5, max(1, base + random.randint(-1, 1))),
            "e3": min(5, max(1, base + random.randint(-1, 1))),
            # Satisfacción
            "s1": min(5, max(1, base + random.randint(-1, 1))),
            "s2": min(5, max(1, base + random.randint(-1, 1))),
            "s3": min(5, max(1, base + random.randint(-1, 1))),
            # Aprendizaje
            "a1": min(5, max(1, base + random.randint(-1, 1))),
            "a2": min(5, max(1, base + random.randint(-1, 1))),
            "a3": min(5, max(1, base + random.randint(-1, 1)))
        }
        
        encuestas.append(encuesta)
    
    return encuestas

print("🔄 Generando datos para Perú...")
envios = generar_envios(100)
encuestas = generar_encuestas(50)

print(f"✅ {len(envios)} envíos generados")
print(f"✅ {len(encuestas)} encuestas generadas\n")

# Insertar envíos
print("📦 Insertando envíos...")
success_envios = 0
for i, envio in enumerate(envios):
    try:
        supabase.table("envios").insert(envio).execute()
        success_envios += 1
        if (i + 1) % 20 == 0:
            print(f"  ✅ {i+1}/{len(envios)} envíos insertados")
    except Exception as e:
        if i == 0:  # Solo mostrar el primer error
            print(f"  ⚠️ Error: {str(e)[:150]}")

# Insertar encuestas
print("\n📋 Insertando encuestas...")
success_encuestas = 0
for i, encuesta in enumerate(encuestas):
    try:
        supabase.table("encuesta_usabilidad").insert(encuesta).execute()
        success_encuestas += 1
        if (i + 1) % 10 == 0:
            print(f"  ✅ {i+1}/{len(encuestas)} encuestas insertadas")
    except Exception as e:
        if i == 0:
            print(f"  ⚠️ Error: {str(e)[:150]}")

print(f"\n🎉 ¡Completado!")
print(f"  ✅ Envíos insertados: {success_envios}/{len(envios)}")
print(f"  ✅ Encuestas insertadas: {success_encuestas}/{len(encuestas)}")

# Verificar totales finales
try:
    total_envios = supabase.table("envios").select("id", count="exact").execute()
    total_encuestas = supabase.table("encuesta_usabilidad").select("id", count="exact").execute()
    print(f"\n📊 Base de datos actualizada:")
    print(f"  - Total envíos: {total_envios.count}")
    print(f"  - Total encuestas: {total_encuestas.count}")
except:
    pass
