# Resultados de Pruebas de Rendimiento - Sistema de Logística

## Métricas por Nivel de Concurrencia

| Hilos (Usuarios Concurrentes) | Total Muestras | Tiempo Promedio (ms) | Tasa de Error (%) | Rendimiento (req/s) |
|-------------------------------|----------------|----------------------|-------------------|---------------------|
|                             1 |             70 |                  150 |               0.0 |                 6.5 |
|                             5 |            350 |                  220 |               0.0 |                22.5 |
|                            10 |            700 |                  380 |               0.0 |                35.0 |
|                            25 |           1750 |                  850 |               2.1 |                45.5 |
|                            50 |           3500 |                 1650 |               8.5 |                42.0 |
|                           100 |           7000 |                 3200 |              18.2 |                38.5 |


---

**Notas:**
- Total Muestras = Hilos × Loops × Páginas (7 páginas probadas)
- Tiempo Promedio: Tiempo de respuesta promedio en milisegundos
- Tasa de Error: Porcentaje de peticiones fallidas
- Rendimiento: Número de peticiones procesadas por segundo (throughput)

⚠️ **ADVERTENCIA:** Los valores mostrados son estimaciones. Para obtener datos reales, ejecutar JMeter.
