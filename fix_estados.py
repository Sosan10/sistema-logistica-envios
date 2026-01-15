from supabase import create_client

SUPABASE_URL = "https://fxvbdigahsnfsnikxrxf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ4dmJkaWdhaHNuZnNuaWt4cnhmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIyODMyODgsImV4cCI6MjA3Nzg1OTI4OH0.ZtAwl8CmqY5yXnjWNWR0j6zhMpc9CcwnqXp4lOLwIYo"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Mapeo de estados antiguos a nuevos (con mayúsculas correctas)
MAPEO_ESTADOS = {
    "creado": "Pendiente",
    "pendiente": "Pendiente",
    "en tránsito": "En tránsito",
    "entregado": "Entregado"
}

print("🔄 Actualizando estados de envíos...")
print("Mapeo:")
for old, new in MAPEO_ESTADOS.items():
    print(f"  '{old}' → '{new}'")

# Obtener todos los envíos
response = supabase.table("envios").select("id, estado").execute()
envios = response.data

print(f"\n📦 Total de envíos a actualizar: {len(envios)}")

# Actualizar cada envío
actualizados = 0
for envio in envios:
    estado_actual = envio['estado']
    
    if estado_actual in MAPEO_ESTADOS:
        nuevo_estado = MAPEO_ESTADOS[estado_actual]
        
        try:
            supabase.table("envios").update({
                "estado": nuevo_estado
            }).eq("id", envio['id']).execute()
            actualizados += 1
            
            if actualizados % 20 == 0:
                print(f"  ✅ Actualizados {actualizados} envíos...")
        except Exception as e:
            print(f"  ⚠️ Error actualizando {envio['id']}: {e}")

print(f"\n✅ Actualización completada: {actualizados} envíos actualizados")

# Verificar la distribución final
print("\n📊 Distribución final de estados:")
response_final = supabase.table("envios").select("estado").execute()
from collections import Counter
estados_finales = Counter([row['estado'] for row in response_final.data])

for estado, cantidad in sorted(estados_finales.items()):
    print(f"  {estado}: {cantidad}")
