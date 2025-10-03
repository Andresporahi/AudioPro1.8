# AudioPro CLI v1.7 - Guía de Usuario

## 🎯 Descripción

AudioPro CLI es una aplicación de línea de comandos para procesar audio y video con Reaper de forma profesional, sin necesidad de interfaz web Streamlit.

## ✨ Características

- ✅ **Procesamiento local** - Funciona completamente en tu máquina sin servidor web
- ✅ **Integración con Reaper** - Usa templates y plugins profesionales de Reaper
- ✅ **ElevenLabs Audio Isolation** - Limpieza profesional de voces (opcional)
- ✅ **Archivos locales** - Procesa archivos desde cualquier ruta en tu sistema
- ✅ **Google Drive** - Descarga y procesa archivos directamente desde Drive
- ✅ **Procesamiento por lotes** - Procesa múltiples archivos desde un archivo de texto
- ✅ **Modo interactivo** - Menú fácil de usar para seleccionar opciones
- ✅ **Modo comandos** - Automatización completa vía argumentos de línea de comandos

## 📋 Requisitos

- Python 3.8+
- FFmpeg instalado y en el PATH
- Reaper instalado
- Template de Reaper configurado
- (Opcional) API Key de ElevenLabs

## 🚀 Instalación

1. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

2. **Verificar FFmpeg:**
```bash
ffmpeg -version
```

3. **Configurar ElevenLabs (opcional):**

Establece las variables de entorno:

**Windows PowerShell:**
```powershell
$env:ELEVENLABS_API_KEY = "tu_api_key_aqui"
```

**Windows CMD:**
```cmd
set ELEVENLABS_API_KEY=tu_api_key_aqui
```

**Linux/Mac:**
```bash
export ELEVENLABS_API_KEY="tu_api_key_aqui"
```

También puedes editar `start_cli.bat` y descomentar las líneas de configuración.

## 🎮 Uso

### Modo 1: Menú Interactivo (Recomendado)

**Windows:**
```bash
start_cli.bat
```

**O directamente con Python:**
```bash
python audiopro_cli.py
```

Esto abrirá un menú interactivo donde puedes:
- Procesar archivos locales
- Procesar archivos de Google Drive
- Procesar lotes de archivos
- Ver configuración actual

### Modo 2: Línea de Comandos

**Procesar un archivo local:**
```bash
python audiopro_cli.py -f "C:\Videos\mi_video.mp4"
```

**Procesar desde Google Drive:**
```bash
python audiopro_cli.py -d "https://drive.google.com/file/d/XXXXX/view"
```

**Procesar lote de archivos:**
```bash
python audiopro_cli.py -b "lista_archivos.txt"
```

**Sin ElevenLabs:**
```bash
python audiopro_cli.py -f "video.mp4" --no-elevenlabs
```

## 📝 Archivo de Lote

Para procesar múltiples archivos, crea un archivo de texto (ej: `archivos.txt`) con una ruta o URL por línea:

```
C:\Videos\video1.mp4
C:\Videos\video2.mp4
https://drive.google.com/file/d/XXXXX/view
F:\Grabaciones\audio.wav
```

Luego procesa el lote:
```bash
python audiopro_cli.py -b archivos.txt
```

## 🎛️ Configuración

La aplicación usa estas rutas por defecto (puedes modificarlas en `audiopro_cli.py`):

- **Reaper EXE:** `C:\Program Files\REAPER (x64)\reaper.exe`
- **Template:** `F:\00\00 Reaper\00 Voces.rpp`
- **Sesiones:** `F:\00\00 Reaper\Procesados`

## 📂 Estructura de Salida

### Archivos Locales
Los archivos procesados se guardan en:
```
[carpeta_original]/procesados/[archivo]_procesado.ext
```

### Archivos de Drive
Los archivos procesados se guardan en:
```
F:\00\00 Reaper\Procesados\[sesion]\[archivo]_procesado.ext
```

### Sesiones de Reaper
Todas las sesiones se guardan en:
```
F:\00\00 Reaper\Procesados\[sesion]\[sesion].rpp
```

## 🔧 Troubleshooting

### FFmpeg no encontrado
```
ERROR: FFmpeg no está instalado o no está en el PATH
```
**Solución:** Instala FFmpeg y agrégalo al PATH del sistema.

### Reaper no abre
**Solución:** Verifica que la ruta a Reaper sea correcta en `audiopro_cli.py`.

### ElevenLabs no funciona
```
API key de ElevenLabs no configurada
```
**Solución:** Establece la variable de entorno `ELEVENLABS_API_KEY` o usa `--no-elevenlabs`.

### Timeout en render
```
Timeout esperando el archivo renderizado
```
**Solución:** El render de Reaper puede tardar. Aumenta el `max_wait` en el código o verifica que Reaper esté procesando correctamente.

## 🎯 Flujo de Procesamiento

1. **Carga del archivo** - Desde ruta local o Google Drive
2. **Extracción de audio** - Conversión a WAV mono 48kHz 16-bit
3. **ElevenLabs (opcional)** - Audio Isolation para limpiar voces
4. **Sesión de Reaper** - Carga en template con plugins profesionales
5. **Render automático** - Reaper procesa con Waves y otros plugins
6. **Mux final** - Si es video, combina audio procesado con video original
7. **Guardado** - Archivo final en carpeta de salida

## 🆚 Diferencias con la Versión Streamlit

| Característica | Streamlit | CLI |
|----------------|-----------|-----|
| Interfaz | Web | Terminal |
| Modo batch | ❌ | ✅ |
| Automatización | ❌ | ✅ |
| Servidor web | ✅ | ❌ |
| Preview multimedia | ✅ | ❌ |
| Portabilidad | Requiere navegador | Totalmente local |

## 💡 Ejemplos de Uso

### Ejemplo 1: Procesar un video local sin ElevenLabs
```bash
python audiopro_cli.py -f "C:\Videos\clase.mp4" --no-elevenlabs
```

### Ejemplo 2: Procesar múltiples archivos de Drive con ElevenLabs
Crea `drive_files.txt`:
```
https://drive.google.com/file/d/ABC123/view
https://drive.google.com/file/d/DEF456/view
https://drive.google.com/file/d/GHI789/view
```

Ejecuta:
```bash
python audiopro_cli.py -b drive_files.txt
```

### Ejemplo 3: Automatización con scripts

**Windows Batch:**
```batch
@echo off
for %%f in (C:\Videos\*.mp4) do (
    python audiopro_cli.py -f "%%f"
)
```

**PowerShell:**
```powershell
Get-ChildItem "C:\Videos\*.mp4" | ForEach-Object {
    python audiopro_cli.py -f $_.FullName
}
```

## 📞 Soporte

Para problemas o sugerencias, revisa la documentación completa del proyecto en `README_v17.md`.

## 🔄 Actualización desde Streamlit

Si estás migrando de la versión Streamlit:

1. Instala colorama: `pip install colorama`
2. Configura variables de entorno para ElevenLabs
3. Usa `audiopro_cli.py` en lugar de `app.py`
4. Todo el procesamiento funciona igual, solo cambia la interfaz

---

**AudioPro CLI v1.7** - Procesamiento Profesional de Audio/Video con Reaper 🎛️


