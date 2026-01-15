# 📊 Cómo Configurar JMeter para Ver Resultados por Nivel de Concurrencia

## ❌ Problema Actual

Si todas las peticiones HTTP tienen el mismo nombre ("Sistema Logística"), JMeter las consolida TODAS en una sola fila, mezclando todos los niveles de usuarios.

## ✅ Solución

Usa **variables de JMeter** para incluir el nombre del Thread Group en cada petición.

### Opción 1: Agregar BeanShell PreProcessor (RÁPIDO)

1. En JMeter, haz clic derecho en **cada Thread Group**
2. Add → Pre Processors → **BeanShell PreProcessor**
3. En el campo "Script", escribe:
   ```java
   vars.put("NIVEL", ctx.getThreadGroup().getName());
   ```
4. Ahora modifica el nombre de cada petición HTTP:
   - En lugar de: `Sistema Logística`
   - Pon: `${NIVEL}`

### Opción 2: Renombrar Manualmente (MÁS SIMPLE)

Para cada Thread Group, cambia el nombre de las peticiones HTTP:

**Thread Group "1 Usuario":**
- Renombra TODAS las peticiones a: `1 Usuario`

**Thread Group "5 Usuarios":**
- Renombra TODAS las peticiones a: `5 Usuarios`

**Thread Group "10 Usuarios":**
- Renombra TODAS las peticiones a: `10 Usuarios`

Y así sucesivamente...

## � Resultado Esperado

Después del cambio, verás en Aggregate Report:

```
Etiqueta         # Muestras    Media    Error %    Throughput
==============================================================
1 Usuario           70           2 ms    0.00%     6.25/sec
5 Usuarios          350          3 ms    0.00%     25.0/sec
10 Usuarios         700          5 ms    0.00%     38.5/sec
25 Usuarios         1750         8 ms    0.00%     52.3/sec
50 Usuarios         3500         12 ms   0.00%     35.8/sec
100 Usuarios        7000         25 ms   0.00%     28.5/sec
```

---

¿Quieres que te genere un nuevo archivo `.jmx` con esta configuración automática, o prefieres hacerlo manualmente en JMeter?
