# Sistema de Logística de Envíos

Sistema de gestión logística desarrollado con Streamlit para el seguimiento y administración de envíos.

## 🚀 Características

- Gestión completa de envíos
- Interfaz web interactiva con Streamlit
- Integración con base de datos
- Pruebas de rendimiento con JMeter
- Generación de reportes y métricas

## 📋 Requisitos

- Python 3.8+
- Dependencias listadas en `requirements.txt` (si existe)

## 🔧 Instalación

1. Clona este repositorio:
```bash
git clone <URL_DEL_REPOSITORIO>
cd Logística
```

2. Crea un entorno virtual:
```bash
python -m venv .venv
```

3. Activa el entorno virtual:
- Windows:
```bash
.venv\Scripts\activate
```
- Linux/Mac:
```bash
source .venv/bin/activate
```

4. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## 🏃 Uso

Ejecuta la aplicación Streamlit:
```bash
streamlit run logistica_envios/app.py
```

## 📊 Pruebas de Rendimiento

El proyecto incluye configuraciones de JMeter para pruebas de rendimiento en el directorio `jmeter/`.

## 📁 Estructura del Proyecto

- `logistica_envios/` - Aplicación principal de Streamlit
- `jmeter/` - Configuraciones y scripts de JMeter
- `generar_tabla_metricas.py` - Script para generar métricas de rendimiento
- `populate_database.py` - Script para poblar la base de datos

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request para sugerencias.

## 📝 Licencia

[Especificar licencia]
