#!/usr/bin/env python
"""
Script para generar la tabla resumen de métricas de rendimiento de JMeter
Muestra: Hilos, Tiempo Promedio, Tasa de Error, y Rendimiento (Throughput)
"""

# Configuración de niveles de prueba según Sistema_PorNivel.jmx
niveles_prueba = [
    {"hilos": 1, "loops": 10, "ramp": 1},
    {"hilos": 5, "loops": 10, "ramp": 2},
    {"hilos": 10, "loops": 10, "ramp": 3},
    {"hilos": 25, "loops": 10, "ramp": 5},
    {"hilos": 50, "loops": 10, "ramp": 10},
    {"hilos": 100, "loops": 10, "ramp": 20},
]

# Número de páginas por prueba (7 páginas del sistema)
PAGINAS_POR_PRUEBA = 7

print("=" * 90)
print(" " * 10 + "📊 TABLA DE MÉTRICAS DE RENDIMIENTO - SISTEMA DE LOGÍSTICA")
print("=" * 90)
print()

# Encabezados
print(f"{'Hilos':>6} | {'Total Muestras':>14} | {'Tiempo Promedio (ms)':>21} | {'Tasa Error (%)':>15} | {'Rendimiento (req/s)':>21}")
print("-" * 90)

# Datos de la tabla
datos_tabla = []

for config in niveles_prueba:
    hilos = config["hilos"]
    loops = config["loops"]
    total_requests = hilos * loops * PAGINAS_POR_PRUEBA
    
    # Estimación de métricas (valores aproximados para pruebas en localhost)
    # Estos valores deberían reemplazarse con resultados reales de JMeter
    
    # Tiempo promedio aumenta con la concurrencia
    if hilos == 1:
        tiempo_promedio_ms = 150
        tasa_error_pct = 0.0
        throughput = 6.5
    elif hilos == 5:
        tiempo_promedio_ms = 220
        tasa_error_pct = 0.0
        throughput = 22.5
    elif hilos == 10:
        tiempo_promedio_ms = 380
        tasa_error_pct = 0.0
        throughput = 35.0
    elif hilos == 25:
        tiempo_promedio_ms = 850
        tasa_error_pct = 2.1
        throughput = 45.5
    elif hilos == 50:
        tiempo_promedio_ms = 1650
        tasa_error_pct = 8.5
        throughput = 42.0
    elif hilos == 100:
        tiempo_promedio_ms = 3200
        tasa_error_pct = 18.2
        throughput = 38.5
    else:
        tiempo_promedio_ms = 0
        tasa_error_pct = 0.0
        throughput = 0
    
    print(f"{hilos:>6} | {total_requests:>14} | {tiempo_promedio_ms:>21} | {tasa_error_pct:>15.1f} | {throughput:>21.1f}")
    
    datos_tabla.append({
        "hilos": hilos,
        "total_muestras": total_requests,
        "tiempo_promedio_ms": tiempo_promedio_ms,
        "tasa_error_pct": tasa_error_pct,
        "throughput": throughput
    })

print("=" * 90)
print()
print("📝 NOTAS:")
print("  - Total Muestras = Hilos × Loops × Páginas (7 páginas por prueba)")
print("  - Tiempo Promedio: Tiempo de respuesta promedio en milisegundos")
print("  - Tasa de Error: Porcentaje de peticiones fallidas")
print("  - Rendimiento: Número de peticiones procesadas por segundo (throughput)")
print()
print("⚠️  ADVERTENCIA: Los valores mostrados son ESTIMACIONES.")
print("   Para obtener datos reales, ejecuta JMeter con:")
print("   jmeter -n -t jmeter\\Sistema_PorNivel.jmx -l resultados.jtl")
print("=" * 90)

# Guardar como CSV
csv_file = "jmeter/tabla_metricas_rendimiento.csv"
with open(csv_file, 'w', encoding='utf-8') as f:
    f.write("Hilos (Usuarios Concurrentes),Total Muestras,Tiempo Promedio (ms),Tasa de Error (%),Rendimiento (req/s)\n")
    for dato in datos_tabla:
        f.write(f"{dato['hilos']},{dato['total_muestras']},{dato['tiempo_promedio_ms']},{dato['tasa_error_pct']},{dato['throughput']}\n")

print(f"\n✅ Tabla guardada en: {csv_file}")

# Crear también una versión para publicación (Markdown)
md_file = "jmeter/tabla_metricas_rendimiento.md"
with open(md_file, 'w', encoding='utf-8') as f:
    f.write("# Resultados de Pruebas de Rendimiento - Sistema de Logística\n\n")
    f.write("## Métricas por Nivel de Concurrencia\n\n")
    f.write("| Hilos (Usuarios Concurrentes) | Total Muestras | Tiempo Promedio (ms) | Tasa de Error (%) | Rendimiento (req/s) |\n")
    f.write("|-------------------------------|----------------|----------------------|-------------------|---------------------|\n")
    for dato in datos_tabla:
        f.write(f"| {dato['hilos']:>29} | {dato['total_muestras']:>14} | {dato['tiempo_promedio_ms']:>20} | {dato['tasa_error_pct']:>17.1f} | {dato['throughput']:>19.1f} |\n")
    f.write("\n\n---\n\n")
    f.write("**Notas:**\n")
    f.write("- Total Muestras = Hilos × Loops × Páginas (7 páginas probadas)\n")
    f.write("- Tiempo Promedio: Tiempo de respuesta promedio en milisegundos\n")
    f.write("- Tasa de Error: Porcentaje de peticiones fallidas\n")
    f.write("- Rendimiento: Número de peticiones procesadas por segundo (throughput)\n\n")
    f.write("⚠️ **ADVERTENCIA:** Los valores mostrados son estimaciones. Para obtener datos reales, ejecutar JMeter.\n")

print(f"✅ Tabla en Markdown guardada en: {md_file}")
