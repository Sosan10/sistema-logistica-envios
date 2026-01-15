from supabase import create_client
import json

SUPABASE_URL = "https://fxvbdigahsnfsnikxrxf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ4dmJkaWdhaHNuZnNuaWt4cnhmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIyODMyODgsImV4cCI6MjA3Nzg1OTI4OH0.ZtAwl8CmqY5yXnjWNWR0j6zhMpc9CcwnqXp4lOLwIYo"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("📋 Analizando esquema de tabla 'envios'...")
response = supabase.table("envios").select("*").limit(1).execute()

if response.data:
    print("\n✅ Registro de ejemplo encontrado:")
    print(json.dumps(response.data[0], indent=2, ensure_ascii=False))
    print("\n📝 Columnas disponibles:", list(response.data[0].keys()))
else:
    print("⚠️ No hay registros en la tabla envios")

print("\n\n📋 Analizando esquema de tabla 'encuesta_usabilidad'...")
response_enc = supabase.table("encuesta_usabilidad").select("*").limit(1).execute()

if response_enc.data:
    print("\n✅ Registro de encuesta encontrado:")
    print(json.dumps(response_enc.data[0], indent=2, ensure_ascii=False))
    print("\n📝 Columnas disponibles:", list(response_enc.data[0].keys()))
else:
    print("⚠️ No hay registros en la tabla encuesta_usabilidad")
