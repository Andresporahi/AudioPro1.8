# 📦 Crear Instalador de AudioPro 1.8

## 🎯 Objetivo

Crear un instalador profesional (.exe) de AudioPro 1.8 que pueda instalarse en cualquier computadora Windows sin necesidad de Python ni dependencias.

---

## 📋 Requisitos Previos

### En tu Computadora (Desarrollo)

1. **Python 3.8+** ✅ (ya lo tienes)
2. **PyInstaller**
3. **Inno Setup 6**
4. **Proyecto AudioPro 1.8** completo

---

## 🚀 Proceso de Instalación

### Paso 1: Instalar PyInstaller

```bash
pip install pyinstaller
```

**Verificar instalación:**
```bash
pyinstaller --version
# Debe mostrar: 5.x.x o superior
```

### Paso 2: Instalar Inno Setup

1. **Descargar** desde: https://jrsoftware.org/isdl.php
2. **Instalar** (siguiente, siguiente, finalizar)
3. **Ruta típica**: `C:\Program Files (x86)\Inno Setup 6\`

---

## 🔨 Crear el Instalador

### Opción 1: Script Automático (Recomendado)

```bash
# Navegar al directorio del proyecto
cd "D:\CURSOR\Audiopro 1.8"

# Ejecutar script de build
build_installer.bat
```

El script automáticamente:
1. ✅ Verifica PyInstaller
2. ✅ Crea el ejecutable con PyInstaller
3. ✅ Verifica Inno Setup
4. ✅ Crea el instalador

**Resultado:**
```
Output\AudioPro_1.8_Setup.exe  (~100-150 MB)
```

### Opción 2: Paso a Paso (Manual)

#### 1. Crear Ejecutable

```bash
cd "D:\CURSOR\Audiopro 1.8"
pyinstaller --clean audiopro_gui.spec
```

**Tiempo estimado:** 2-5 minutos

**Output:**
```
dist\AudioPro\
├── AudioPro.exe           ← Ejecutable principal
├── python313.dll
├── _internal\             ← Librerías
└── *.lua                  ← Scripts Reaper
```

#### 2. Probar el Ejecutable

```bash
cd dist\AudioPro
AudioPro.exe
```

**Verificar:**
- ✅ Se abre la interfaz gráfica
- ✅ Botones funcionan
- ✅ No hay errores en consola

#### 3. Crear Instalador

```bash
# Desde la raíz del proyecto
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" audiopro_installer.iss
```

**Tiempo estimado:** 30-60 segundos

**Output:**
```
Output\AudioPro_1.8_Setup.exe
```

---

## 📦 Contenido del Instalador

### Archivos Incluidos

```
AudioPro\ (carpeta de instalación)
├── AudioPro.exe                    ← Ejecutable principal
├── python313.dll                   ← Python runtime
├── _internal\                      ← Dependencias Python
│   ├── audio_utils_cli.pyc
│   ├── tkinter\
│   ├── requests\
│   └── ...
├── add_multiple_media.lua          ← Script Reaper batch
├── add_audio_to_session.lua        ← Script Reaper individual
├── render_session.lua              ← Utilidades Reaper
├── test_reaper.lua                 ← Script de pruebas
├── README.md                       ← Documentación principal
├── VERSION_1.8.md                  ← Notas de versión
├── CALIDAD_SIN_PERDIDA.md          ← Guía de calidad
├── VIDEO_TIMELINE_RENDER.md        ← Guía de video
├── PROCESAMIENTO_BATCH.md          ← Guía de batch
├── INSTALACION_COMPLETA.md         ← Guía de instalación
├── requirements.txt                ← Lista de dependencias
├── config.ini                      ← Configuración (creado en instalación)
└── temp\                           ← Carpeta temporal
```

### Tamaño del Instalador

- **Tamaño comprimido (Setup.exe):** ~80-120 MB
- **Tamaño instalado:** ~200-300 MB
- **Depende de:** Python runtime + dependencias

---

## ⚙️ Configuración Durante la Instalación

### El instalador preguntará:

1. **Directorio de instalación**
   - Por defecto: `C:\Program Files\AudioPro`
   - Puedes cambiar a cualquier ubicación

2. **Ruta de Reaper**
   - Por defecto: `C:\Program Files\REAPER (x64)\reaper.exe`
   - Ajustar si Reaper está en otra ubicación

3. **Directorio de sesiones**
   - Por defecto: `F:\00\00 Reaper\Procesados`
   - Donde se guardarán los proyectos de Reaper

4. **Template de Reaper**
   - Por defecto: `F:\00\00 Reaper\00 Voces.rpp`
   - Tu template personalizado de Reaper

5. **Accesos directos**
   - ✅ Menú Inicio
   - ☐ Escritorio (opcional)
   - ☐ Barra de tareas (opcional)

---

## 📝 Notas Sobre el Instalador

### ✅ Lo que Incluye

- ✅ AudioPro ejecutable
- ✅ Python runtime embebido
- ✅ Todas las dependencias Python
- ✅ Scripts Lua para Reaper
- ✅ Documentación completa
- ✅ Configuración automática

### ❌ Lo que NO Incluye (debe instalarse por separado)

- ❌ **Reaper** - Descargar de https://www.reaper.fm
- ❌ **FFmpeg** - AudioPro lo descarga automáticamente al primer uso
- ❌ Template de Reaper personalizado (usar el propio)

---

## 🎯 Distribuir el Instalador

### Subir a GitHub Release

```bash
# 1. Crear tag de versión
git tag -a v1.8 -m "AudioPro 1.8 - Procesamiento por lotes con video"
git push origin v1.8

# 2. Ir a GitHub > Releases > Create new release
# 3. Subir: Output\AudioPro_1.8_Setup.exe
# 4. Agregar notas de versión desde VERSION_1.8.md
```

### Compartir Directamente

El archivo `AudioPro_1.8_Setup.exe` es **standalone** y puede compartirse por:
- Google Drive
- Dropbox
- OneDrive
- WeTransfer
- USB

---

## 🖥️ Instalar en Otra Computadora

### Requisitos en PC Destino

**Hardware:**
- Windows 10/11 (64-bit)
- 4GB RAM mínimo (8GB recomendado)
- 500MB espacio libre
- Conexión a internet (para descargar FFmpeg)

**Software:**
- ✅ Reaper instalado
- ✅ Template de Reaper configurado
- ❌ NO necesita Python
- ❌ NO necesita instalar dependencias

### Proceso de Instalación

1. **Ejecutar instalador**
   ```
   AudioPro_1.8_Setup.exe
   ```

2. **Seguir asistente**
   - Aceptar términos
   - Elegir directorio
   - Configurar rutas de Reaper
   - Crear accesos directos

3. **Finalizar**
   - Click en "Finalizar"
   - Opcionalmente: "Ejecutar AudioPro"

4. **Primera ejecución**
   - AudioPro detectará que falta FFmpeg
   - Descargará FFmpeg automáticamente
   - Configurará rutas de Reaper

---

## 🔧 Solución de Problemas

### Error: "PyInstaller not found"

**Solución:**
```bash
pip install pyinstaller
```

### Error: "Inno Setup not found"

**Solución:**
1. Descargar de https://jrsoftware.org/isdl.php
2. Instalar en `C:\Program Files (x86)\Inno Setup 6\`
3. Ejecutar script nuevamente

### Error: "Module not found" al ejecutar .exe

**Causa:** Falta alguna dependencia en `hiddenimports`

**Solución:** Editar `audiopro_gui.spec`, agregar módulo faltante:
```python
hiddenimports = [
    'audio_utils_cli',
    'modulo_faltante',  # ← Agregar aquí
]
```

Luego reconstruir:
```bash
pyinstaller --clean audiopro_gui.spec
```

### Instalador muy grande (>200 MB)

**Causa:** PyInstaller incluye todas las dependencias

**Solución (opcional):** Optimizar excluyendo módulos no usados:
```python
# En audiopro_gui.spec, agregar a excludes:
excludes=[
    'matplotlib',
    'numpy',
    'scipy',
    'pandas',
]
```

---

## 📊 Comparación de Opciones

| Método | Tamaño | Facilidad | Portabilidad |
|--------|--------|-----------|--------------|
| **Instalador (.exe)** | ~100MB | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Ejecutable solo | ~200MB | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Carpeta dist\ | ~300MB | ⭐⭐⭐ | ⭐⭐⭐ |
| Script Python | ~1MB | ⭐⭐ | ⭐ |

**Recomendación:** Usar instalador para distribución profesional.

---

## 🎓 Mejoras Futuras

### V1.9 - Instalador Mejorado

- [ ] Ícono personalizado (.ico)
- [ ] Firma digital del ejecutable
- [ ] Descarga automática de FFmpeg en instalación
- [ ] Detección automática de Reaper instalado
- [ ] Opción de instalación portable (sin registry)
- [ ] Actualizador automático

### Ícono Personalizado

1. **Crear ícono:**
   - Diseñar logo de AudioPro
   - Convertir a .ico (256x256, 128x128, 64x64, 32x32, 16x16)

2. **Usar en PyInstaller:**
   ```python
   # En audiopro_gui.spec
   exe = EXE(
       ...
       icon='audiopro_icon.ico',  # ← Agregar esta línea
   )
   ```

3. **Usar en Inno Setup:**
   ```ini
   ; En audiopro_installer.iss
   SetupIconFile=audiopro_icon.ico
   ```

---

## ✅ Checklist Final

Antes de distribuir, verificar:

- [ ] El ejecutable se abre correctamente
- [ ] Todos los botones funcionan
- [ ] Puede agregar archivos (locales y Drive)
- [ ] Puede procesar archivos de prueba
- [ ] Scripts Lua están incluidos
- [ ] Documentación está incluida
- [ ] El instalador crea accesos directos
- [ ] El instalador crea config.ini correctamente
- [ ] Se puede desinstalar limpiamente

---

## 📚 Recursos Adicionales

- **PyInstaller Docs:** https://pyinstaller.org/en/stable/
- **Inno Setup Docs:** https://jrsoftware.org/ishelp/
- **Python Packaging:** https://packaging.python.org/
- **GitHub Releases:** https://docs.github.com/en/repositories/releasing-projects-on-github

---

## 🎉 Resumen

Para crear el instalador:

```bash
# 1. Instalar herramientas (solo una vez)
pip install pyinstaller
# Descargar Inno Setup de https://jrsoftware.org/isdl.php

# 2. Crear instalador (cada versión)
cd "D:\CURSOR\Audiopro 1.8"
build_installer.bat

# 3. Resultado
Output\AudioPro_1.8_Setup.exe  ← ¡Listo para distribuir!
```

**Tiempo total:** 5-10 minutos
**Tamaño final:** ~100 MB
**Compatible:** Windows 10/11 (64-bit)

---

**AudioPro 1.8** 📦 - Instalador Profesional Listo

*"Distribúyelo en cualquier PC con un solo click"*

