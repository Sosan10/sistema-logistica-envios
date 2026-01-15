"""
Generador de archivo JMX con nombres únicos por nivel de concurrencia
"""

def generar_jmx_con_nombres_unicos():
    niveles = [
        {'nombre': '1 Usuario', 'hilos': 1, 'ramp': 1},
        {'nombre': '5 Usuarios', 'hilos': 5, 'ramp': 2},
        {'nombre': '10 Usuarios', 'hilos': 10, 'ramp': 3},
        {'nombre': '25 Usuarios', 'hilos': 25, 'ramp': 5},
        {'nombre': '50 Usuarios', 'hilos': 50, 'ramp': 10},
        {'nombre': '100 Usuarios', 'hilos': 100, 'ramp': 20}
    ]
    
    paginas = ['/', '/Gestion_Envios', '/Seguimiento', '/Analisis', '/Encuestas', '/Resultados', '/Configuracion']
    
    jmx = '''<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2" properties="5.0" jmeter="5.6.3">
  <hashTree>
    <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="Sistema Logística - Por Nivel">
      <stringProp name="TestPlan.comments">Resultados separados por nivel de concurrencia</stringProp>
      <boolProp name="TestPlan.serialize_threadgroups">true</boolProp>
      <elementProp name="TestPlan.user_defined_variables" elementType="Arguments">
        <collectionProp name="Arguments.arguments">
          <elementProp name="HOST" elementType="Argument">
            <stringProp name="Argument.value">localhost</stringProp>
          </elementProp>
          <elementProp name="PORT" elementType="Argument">
            <stringProp name="Argument.value">8501</stringProp>
          </elementProp>
        </collectionProp>
      </elementProp>
    </TestPlan>
    <hashTree>
'''
    
    for nivel in niveles:
        jmx += f'''
      <ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="{nivel['nombre']}">
        <intProp name="ThreadGroup.num_threads">{nivel['hilos']}</intProp>
        <intProp name="ThreadGroup.ramp_time">{nivel['ramp']}</intProp>
        <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
        <elementProp name="ThreadGroup.main_controller" elementType="LoopController" guiclass="LoopControlPanel" testclass="LoopController">
          <stringProp name="LoopController.loops">10</stringProp>
        </elementProp>
      </ThreadGroup>
      <hashTree>
'''
        for pagina in paginas:
            # CLAVE: Cada petición tiene el nombre del Thread Group
            jmx += f'''
        <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="{nivel['nombre']}">
          <stringProp name="HTTPSampler.domain">${{HOST}}</stringProp>
          <stringProp name="HTTPSampler.port">${{PORT}}</stringProp>
          <stringProp name="HTTPSampler.path">{pagina}</stringProp>
          <stringProp name="HTTPSampler.method">GET</stringProp>
        </HTTPSamplerProxy>
        <hashTree/>
'''
        
        jmx += '''
      </hashTree>
'''
    
    jmx += '''
      <ResultCollector guiclass="StatVisualizer" testclass="ResultCollector" testname="📊 Aggregate Report">
        <boolProp name="ResultCollector.error_logging">false</boolProp>
        <objProp>
          <name>saveConfig</name>
          <value class="SampleSaveConfiguration">
            <time>true</time>
            <latency>true</latency>
            <timestamp>true</timestamp>
            <success>true</success>
            <label>true</label>
            <code>true</code>
            <message>true</message>
            <threadName>true</threadName>
            <bytes>true</bytes>
            <sentBytes>true</sentBytes>
          </value>
        </objProp>
        <stringProp name="filename"></stringProp>
      </ResultCollector>
      <hashTree/>
      
      <ResultCollector guiclass="SimpleDataWriter" testclass="ResultCollector" testname="💾 Resultados">
        <stringProp name="filename">resultados_por_nivel.jtl</stringProp>
      </ResultCollector>
      <hashTree/>
      
    </hashTree>
  </hashTree>
</jmeterTestPlan>
'''
    
    return jmx

# Generar y guardar
with open('Sistema_PorNivel.jmx', 'w', encoding='utf-8') as f:
    f.write(generar_jmx_con_nombres_unicos())

print("✅ Archivo generado: Sistema_PorNivel.jmx")
print()
print("En este archivo, verás 6 filas en Aggregate Report:")
print("  - 1 Usuario")
print("  - 5 Usuarios")  
print("  - 10 Usuarios")
print("  - 25 Usuarios")
print("  - 50 Usuarios")
print("  - 100 Usuarios")
