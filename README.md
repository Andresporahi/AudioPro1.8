# 🎛️ AudioPro 1.8 - Procesamiento Profesional con Reaper

**Versión 1.8** - Sistema de Procesamiento por Lotes

## 📋 Descripción

AudioPro 1.8 es una aplicación profesional de procesamiento de audio que integra **Reaper** para aplicar efectos y normalización de audio de forma automatizada. Esta versión introduce el **procesamiento por lotes**, permitiendo procesar múltiples archivos de forma eficiente.

### ✨ Novedades en v1.8

- 🚀 **Procesamiento por Lotes**: Procesa múltiples archivos hasta 70% más rápido
- 📊 **Timeline Secuencial**: Los archivos se insertan secuencialmente en Reaper sin superposiciones
- 📁 **Carpeta Automática**: Todos los archivos procesados se guardan en carpeta `procesados/`
- 🎨 **Interfaz Moderna**: Diseño actualizado con colores de Platzi
- ⚡ **Mejor Rendimiento**: Un solo proceso de Reaper para múltiples archivos

## 🎯 Características

### 🖥️ Dos Interfaces Disponibles

1. **GUI (Interfaz Gráfica)** 🎨
   - Interfaz moderna con colores de Platzi
   - Arrastrar y soltar múltiples archivos
   - Log en tiempo real
   - Fácil de usar

2. **CLI (Línea de Comandos)** ⌨️
   - Procesamiento por lotes desde terminal
   - Ideal para automatización
   - Soporte para archivos desde rutas o archivo de texto

### 🎛️ Procesamiento Profesional

- **Normalización de Audio**: Ajuste automático a -16 LUFS
- **Sample Rate**: Conversión a 48kHz
- **Formato de Salida**: WAV Mono 24-bit PCM
- **ElevenLabs Integration**: Audio isolation opcional (requiere API key)
- **Soporte Multi-formato**: MP4, MP3, WAV, AVI, MOV, MKV, M4A, FLAC

### 🔄 Flujo de Trabajo por Lotes

```
Fase 1 - Preparación:
  → Extracción de audio de videos
  → Procesamiento con ElevenLabs (opcional)
  → Conversión a formato WAV compatible

Fase 2 - Procesamiento en Reaper:
  → Inserción secuencial en timeline
  → Aplicación de efectos y normalización
  → Render individual de cada archivo

Fase 3 - Resultado:
  → Archivos guardados en carpeta "procesados"
  → Nombrado automático con sufijo "_procesado"
```

## 🚀 Instalación

### Requisitos Previos

1. **Python 3.8+**
2. **FFmpeg** (incluido en el proyecto)
3. **Reaper** instalado en: `C:\Program Files\REAPER (x64)\reaper.exe`
4. **Template de Reaper** con pista llamada "Clase"

### Instalación Rápida

```bash
# 1. Clonar repositorio
git clone https://github.com/Andresporahi/AudioPro1.8.git
cd AudioPro1.8

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. (Opcional) Configurar ElevenLabs
# Crear archivo .env con:
# ELEVENLABS_API_KEY=tu_api_key_aqui
```

### Crear Accesos Directos

```bash
# Ejecutar como administrador
Instalar_Accesos_Directos.bat
```

Esto creará accesos directos en tu escritorio para:
- 🎨 **AudioPro GUI**: Interfaz gráfica
- ⌨️ **AudioPro CLI**: Interfaz de comandos
- 🚀 **AudioPro Launcher**: Selector de interfaz

## 📖 Uso

### 🎨 Interfaz Gráfica (Recomendado)

```bash
# Opción 1: Usar launcher
AudioPro_Launcher.bat

# Opción 2: Abrir GUI directamente
AudioPro_GUI.bat

# Opción 3: Con Python
python audiopro_gui.py
```

**Pasos en la GUI:**

1. Click en "📂 Agregar Varios Archivos" para seleccionar múltiples archivos
2. (Opcional) Activar "✨ ElevenLabs Audio Isolation"
3. Click en "🎛️ PROCESAR CON REAPER"
4. Esperar a que termine el procesamiento
5. Los archivos procesados estarán en la carpeta `procesados/`

### ⌨️ Línea de Comandos

```bash
# Procesar un archivo
python audiopro_cli.py -f "ruta/al/archivo.mp4"

# Procesar múltiples archivos
python audiopro_cli.py -f "archivo1.mp4" "archivo2.mp3" "archivo3.wav"

# Procesar desde lista de archivos
python audiopro_cli.py -l archivos.txt

# Con ElevenLabs
python audiopro_cli.py -f "archivo.mp4" --elevenlabs

# Desde Google Drive
python audiopro_cli.py -d "https://drive.google.com/file/d/..."
```

## 📁 Estructura del Proyecto

```
AudioPro1.8/
├── 📄 audiopro_gui.py           # Interfaz gráfica principal
├── 📄 audiopro_cli.py           # Interfaz de línea de comandos
├── 📄 audio_utils_cli.py        # Utilidades de audio
├── 🎵 add_multiple_audios.lua   # Script Reaper para batch
├── 🎵 add_audio_to_session.lua  # Script Reaper individual
├── 📦 requirements.txt          # Dependencias Python
├── 🚀 AudioPro_GUI.bat          # Launcher GUI
├── 🚀 AudioPro_CLI.bat          # Launcher CLI
├── 🚀 AudioPro_Launcher.bat     # Launcher principal
├── 📖 README.md                 # Este archivo
├── 📖 PROCESAMIENTO_BATCH.md    # Documentación técnica batch
├── 📖 CAMBIO_PROCESAMIENTO_BATCH.md  # Resumen de cambios v1.8
├── 📖 README_CLI.md             # Documentación CLI
├── 📖 GUIA_RAPIDA.md            # Guía de inicio rápido
└── 📖 GUIA_COMPLETA_INTERFACES.md  # Guía completa GUI + CLI
```

## ⚙️ Configuración

### Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
# ElevenLabs (Opcional)
ELEVENLABS_API_KEY=tu_api_key_aqui
ELEVENLABS_BASE_URL=https://api.elevenlabs.io

# Rutas Reaper (Opcional - valores por defecto)
REAPER_EXE=C:\Program Files\REAPER (x64)\reaper.exe
REAPER_TEMPLATE=F:\00\00 Reaper\00 Voces.rpp
REAPER_SESSIONS_DIR=F:\00\00 Reaper\Procesados
```

### Configuración de Reaper

Tu template de Reaper debe tener:
- Una pista llamada "Clase" (o "clase", es case-insensitive)
- Efectos y plugins configurados en el master o en la pista "Clase"
- Normalización configurada en el master

## 📊 Rendimiento

### Tiempos de Procesamiento

| Archivos | v1.7 (Individual) | v1.8 (Batch) | Mejora |
|----------|-------------------|--------------|--------|
| 1 archivo | ~30s | ~30s | 0% |
| 3 archivos | ~90s | ~40s | **55%** |
| 10 archivos | ~300s | ~90s | **70%** |

## 🎯 Casos de Uso

### 📚 Procesamiento de Clases Online

```bash
# Procesar múltiples videos de clases
python audiopro_cli.py -f clase1.mp4 clase2.mp4 clase3.mp4 --elevenlabs
```

Resultado: Audios normalizados, sin ruido, listos para publicar.

### 🎙️ Podcasts

```bash
# Procesar episodios de podcast
python audiopro_cli.py -f episodio1.mp3 episodio2.mp3 episodio3.mp3
```

Resultado: Episodios con volumen consistente y calidad profesional.

### 🎬 Post-Producción de Video

```bash
# Procesar audios de múltiples videos
python audiopro_cli.py -l lista_videos.txt --elevenlabs
```

Resultado: Audios limpios listos para mezclar con video.

## 🐛 Solución de Problemas

### ⚠️ "No se encontró la pista 'Clase'"

**Causa**: Tu template de Reaper no tiene una pista llamada "Clase".

**Solución**: 
1. Abre Reaper
2. Carga tu template
3. Renombra una pista a "Clase"
4. Guarda el template

### ⚠️ "Permission denied" en archivos

**Causa**: Reaper aún tiene el archivo abierto.

**Solución**: El script espera automáticamente. Si persiste, cierra Reaper manualmente.

### ⚠️ "Timeout esperando render"

**Causa**: El archivo es muy largo (>60 segundos de procesamiento).

**Solución**: Revisa la carpeta `procesados/` - el archivo probablemente se renderizó correctamente.

### ⚠️ FFmpeg no encontrado

**Solución**:
```bash
python setup_ffmpeg.py
```

## 📝 Notas Importantes

1. **Archivos Temporales**: Se crean automáticamente y se eliminan al finalizar
2. **ElevenLabs**: Consume créditos de API por archivo procesado
3. **Carpeta Procesados**: Se crea en la ubicación del primer archivo
4. **Sesión Reaper**: Se guarda con nombre único para revisión posterior

## 🤝 Contribuir

¿Encontraste un bug? ¿Tienes una sugerencia? 

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📜 Licencia

Este proyecto es privado. Todos los derechos reservados.

## 👨‍💻 Autor

**Andresporahi**

- GitHub: [@Andresporahi](https://github.com/Andresporahi)
- Proyecto: [AudioPro1.8](https://github.com/Andresporahi/AudioPro1.8)

## 📚 Documentación Adicional

- [📖 Procesamiento por Lotes](PROCESAMIENTO_BATCH.md) - Documentación técnica completa
- [📖 Cambios v1.8](CAMBIO_PROCESAMIENTO_BATCH.md) - Resumen de cambios y mejoras
- [📖 Guía CLI](README_CLI.md) - Uso detallado de línea de comandos
- [📖 Guía Rápida](GUIA_RAPIDA.md) - Inicio rápido
- [📖 Guía Completa](GUIA_COMPLETA_INTERFACES.md) - GUI + CLI completo

## 🎉 Agradecimientos

- **Reaper** por su excelente API de scripting
- **FFmpeg** por las capacidades de procesamiento multimedia
- **ElevenLabs** por la tecnología de audio isolation
- **Platzi** por la inspiración del diseño

---

**AudioPro 1.8** 🎛️ - Procesamiento Profesional con Reaper por Lotes

*Desarrollado con ❤️ para profesionales de audio*
