# Guía de Contribución

¡Gracias por tu interés en contribuir al Sistema de Logística y Seguimiento de Envíos! 🚀

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [¿Cómo Puedo Contribuir?](#cómo-puedo-contribuir)
- [Proceso de Desarrollo](#proceso-de-desarrollo)
- [Guías de Estilo](#guías-de-estilo)
- [Reportar Bugs](#reportar-bugs)
- [Sugerir Mejoras](#sugerir-mejoras)

## 📜 Código de Conducta

Este proyecto se adhiere a un código de conducta. Al participar, se espera que mantengas este código. Por favor, reporta comportamientos inaceptables.

## 🤝 ¿Cómo Puedo Contribuir?

### Reportar Bugs

Los bugs se rastrean como [GitHub Issues](https://github.com/Sosan10/sistema-logistica-envios/issues). Antes de crear un issue:

1. **Verifica** que el bug no haya sido reportado previamente
2. **Incluye** información detallada:
   - Descripción clara del problema
   - Pasos para reproducir
   - Comportamiento esperado vs. actual
   - Screenshots si es aplicable
   - Información del entorno (OS, versión de Python, etc.)

### Sugerir Mejoras

Las sugerencias de mejoras también se rastrean como GitHub Issues. Para sugerir una mejora:

1. **Describe** claramente la funcionalidad propuesta
2. **Explica** por qué sería útil
3. **Proporciona** ejemplos de uso si es posible

### Pull Requests

1. Fork el repositorio
2. Crea una rama desde `main`:
   ```bash
   git checkout -b feature/mi-nueva-funcionalidad
   ```
3. Realiza tus cambios
4. Asegúrate de que el código siga las guías de estilo
5. Commit tus cambios con mensajes descriptivos
6. Push a tu fork
7. Abre un Pull Request

## 🔄 Proceso de Desarrollo

### Configuración del Entorno

```bash
# Clonar tu fork
git clone https://github.com/TU-USUARIO/sistema-logistica-envios.git
cd sistema-logistica-envios

# Agregar el repositorio original como remote
git remote add upstream https://github.com/Sosan10/sistema-logistica-envios.git

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### Mantener tu Fork Actualizado

```bash
git fetch upstream
git checkout main
git merge upstream/main
```

## 📝 Guías de Estilo

### Código Python

- Sigue [PEP 8](https://pep8.org/)
- Usa nombres descriptivos para variables y funciones
- Documenta funciones complejas con docstrings
- Mantén las funciones pequeñas y enfocadas

Ejemplo:
```python
def calcular_costo_envio(peso: float, distancia: float) -> float:
    """
    Calcula el costo de envío basado en peso y distancia.
    
    Args:
        peso (float): Peso del paquete en kg
        distancia (float): Distancia en km
        
    Returns:
        float: Costo calculado en soles
    """
    costo_base = 10.0
    costo_por_kg = 2.5
    costo_por_km = 0.5
    
    return costo_base + (peso * costo_por_kg) + (distancia * costo_por_km)
```

### Commits

Usa mensajes de commit descriptivos siguiendo [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Cambios en documentación
- `style:` Cambios de formato (no afectan el código)
- `refactor:` Refactorización de código
- `test:` Agregar o modificar tests
- `chore:` Tareas de mantenimiento

Ejemplos:
```
feat: Agregar módulo de notificaciones por email
fix: Corregir cálculo de fecha estimada de entrega
docs: Actualizar guía de instalación en README
```

### Documentación

- Actualiza el README.md si agregas nuevas funcionalidades
- Documenta cambios en la API o configuración
- Incluye ejemplos de uso cuando sea relevante

## 🐛 Reportar Bugs

### Antes de Reportar

- Verifica que estás usando la última versión
- Busca en issues existentes
- Intenta reproducir el bug en un entorno limpio

### Template de Bug Report

```markdown
**Descripción del Bug**
Una descripción clara y concisa del bug.

**Pasos para Reproducir**
1. Ve a '...'
2. Haz click en '...'
3. Scroll hasta '...'
4. Ver error

**Comportamiento Esperado**
Descripción de lo que esperabas que sucediera.

**Screenshots**
Si aplica, agrega screenshots.

**Entorno:**
 - OS: [e.g. Windows 10]
 - Python: [e.g. 3.9.7]
 - Streamlit: [e.g. 1.28.0]

**Contexto Adicional**
Cualquier otra información relevante.
```

## 💡 Sugerir Mejoras

### Template de Feature Request

```markdown
**¿Tu solicitud está relacionada con un problema?**
Descripción clara del problema. Ej: "Siempre me frustra cuando..."

**Describe la solución que te gustaría**
Descripción clara de lo que quieres que suceda.

**Describe alternativas que has considerado**
Descripción de soluciones o funcionalidades alternativas.

**Contexto Adicional**
Cualquier otra información o screenshots.
```

## ✅ Checklist para Pull Requests

Antes de enviar tu PR, asegúrate de:

- [ ] El código sigue las guías de estilo del proyecto
- [ ] Has realizado una auto-revisión de tu código
- [ ] Has comentado tu código, especialmente en áreas difíciles
- [ ] Has actualizado la documentación correspondiente
- [ ] Tus cambios no generan nuevas advertencias
- [ ] Has probado que tu código funciona correctamente
- [ ] El título del PR sigue Conventional Commits

## 🎯 Áreas donde Puedes Contribuir

- **Nuevas Funcionalidades**: Agregar módulos o características
- **Mejoras de UI/UX**: Mejorar la interfaz de usuario
- **Optimización**: Mejorar el rendimiento del código
- **Documentación**: Mejorar o traducir documentación
- **Tests**: Agregar pruebas unitarias o de integración
- **Bug Fixes**: Corregir bugs reportados

## 📞 ¿Preguntas?

Si tienes preguntas sobre cómo contribuir, puedes:

1. Abrir un [GitHub Issue](https://github.com/Sosan10/sistema-logistica-envios/issues)
2. Contactar al mantenedor: ysolorzano@unitru.edu.pe

---

¡Gracias por contribuir! 🙌
