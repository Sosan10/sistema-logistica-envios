from supabase import create_client
import sys

SUPABASE_URL = "https://fxvbdigahsnfsnikxrxf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ4dmJkaWdhaHNuZnNuaWt4cnhmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIyODMyODgsImV4cCI6MjA3Nzg1OTI4OH0.ZtAwl8CmqY5yXnjWNWR0j6zhMpc9CcwnqXp4lOLwIYo"

print("🔍 Probando conexión a Supabase...")
print(f"URL: {SUPABASE_URL}")

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Cliente de Supabase creado exitosamente")
    
    # Probar consulta a la tabla envios
    print("\n📊 Probando consulta a tabla 'envios'...")
    response = supabase.table("envios").select("*").limit(5).execute()
    
    if response.data:
        print(f"✅ Conexión exitosa! Se encontraron {len(response.data)} registros")
        print(f"Columnas disponibles: {list(response.data[0].keys()) if response.data else 'N/A'}")
    else:
        print("⚠️ Conexión exitosa pero no hay datos en la tabla 'envios'")
    
    # Probar tabla de encuestas
    print("\n📋 Probando consulta a tabla 'encuesta_usabilidad'...")
    response_encuesta = supabase.table("encuesta_usabilidad").select("*").limit(5).execute()
    
    if response_encuesta.data:
        print(f"✅ Tabla de encuestas encontrada con {len(response_encuesta.data)} registros")
    else:
        print("⚠️ Tabla 'encuesta_usabilidad' existe pero está vacía")
        
    print("\n🎉 CONEXIÓN A SUPABASE EXITOSA!")
    sys.exit(0)
    
except Exception as e:
    print(f"\n❌ Error al conectar con Supabase: {type(e).__name__}")
    print(f"Detalles: {str(e)}")
    sys.exit(1)
