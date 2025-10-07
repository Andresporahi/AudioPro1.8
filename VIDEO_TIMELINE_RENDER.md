# 🎬 AudioPro 1.8 - Procesamiento de Video en Timeline

## ✨ Nueva Funcionalidad: Videos en Reaper

Ahora AudioPro puede importar **videos completos** directamente al timeline de Reaper, no solo el audio. Esto te permite ver y procesar el video junto con el audio en una sola sesión.

---

## 🎯 ¿Cómo Funciona?

### Flujo de Trabajo

```
1. Seleccionar Videos/Audios en la GUI
   ↓
2. Los archivos se copian a ubicación accesible por Reaper
   ↓
3. Se importan al timeline secuencialmente
   |--- Video 1 ---|--- Audio 1 ---|--- Video 2 ---|
   0s               120s            180s           300s
   ↓
4. Reaper procesa cada archivo con efectos/normalización
   ↓
5. Renderiza individualmente:
   - Videos → MP4 con audio procesado
   - Audios → WAV 48kHz 24-bit Mono
   ↓
6. Resultados en carpeta "procesados"
```

---

## 📊 Ejemplo Práctico

### Caso 1: Procesamiento Mixto

**Input:**
- `clase1.mp4` (video 5 min)
- `intro.mp3` (audio 30 seg)
- `clase2.mp4` (video 10 min)

**Proceso:**

1. **Timeline de Reaper:**
```
Pista "Clase":
|--- clase1.mp4 ---|--- intro.mp3 ---|--- clase2.mp4 ---|
0:00               5:00             5:30              15:30
```

2. **Renders Individuales:**
```
procesados/
├── clase1_procesado.mp4     ← Video completo con audio mejorado
├── intro_procesado.wav      ← Audio procesado
└── clase2_procesado.mp4     ← Video completo con audio mejorado
```

---

## 🔧 Características Técnicas

### Detección Automática

El sistema detecta automáticamente el tipo de archivo:

```python
Extensiones de Video: .mp4, .avi, .mov, .mkv, .wmv, .flv, .webm
Extensiones de Audio: .mp3, .wav, .flac, .m4a, .aac, .ogg
```

### Configuración de Render

#### Para Videos
```lua
-- Reaper Video Settings
- Sample Rate: 48kHz
- Channels: Stereo (2)
- Format: MP4 (mantiene codec original del video)
- Video: Incluido en render
- Audio: Procesado con efectos de Reaper
- Timeout: 120 segundos (videos tardan más)
```

#### Para Audios
```lua
-- Reaper Audio Settings
- Sample Rate: 48kHz
- Channels: Mono (1)
- Format: WAV 24-bit PCM
- Timeout: 60 segundos
```

---

## 🎛️ Ventajas del Timeline en Reaper

### 1. **Visualización Completa**
- Puedes ver la forma de onda de cada archivo
- Para videos, ves también el video en la ventana de video de Reaper
- Identificar fácilmente problemas de audio

### 2. **Edición Manual Posible**
- Si necesitas ajustar algo, la sesión queda guardada
- Puedes editar manualmente en Reaper después
- Re-renderizar cuando quieras

### 3. **Procesamiento Consistente**
- Todos los archivos pasan por los mismos efectos
- Normalización uniforme (-16 LUFS)
- Calidad consistente en toda la producción

### 4. **Eficiencia**
- Un solo proyecto de Reaper para todos los archivos
- No abrir/cerrar Reaper múltiples veces
- Timeline secuencial sin gaps

---

## 📁 Estructura de Archivos

### Durante el Procesamiento

```
F:\00\00 Reaper\
├── Eleven\
│   ├── video_20251003_201500.mp4  ← Copia temporal
│   └── video_20251003_201530.mp4  ← Copia temporal
│
├── Procesados\
│   ├── AudioPro_Batch_20251003_201500.rpp  ← Sesión Reaper
│   └── procesados\
│       ├── clase1_procesado.mp4  ← OUTPUT VIDEO
│       ├── intro_procesado.wav   ← OUTPUT AUDIO
│       └── clase2_procesado.mp4  ← OUTPUT VIDEO
```

### Limpieza Automática
- Las copias temporales en `Eleven\` se eliminan al finalizar
- Los archivos procesados permanecen en `procesados\`
- La sesión de Reaper se conserva para revisión

---

## 🎥 Calidad de Video

### Video Stream
- ✅ **NO se recodifica** desde Reaper
- ✅ **Mantiene codec original** (H.264, H.265, etc.)
- ✅ **Calidad visual idéntica** al original
- ✅ **Resolución preservada** (1080p, 4K, etc.)

### Audio Stream
- ✅ **Procesado con efectos** de Reaper
- ✅ **Normalizado** a -16 LUFS
- ✅ **Limpiado** de ruido
- ✅ **Alta calidad** (AAC o según template)

---

## ⚙️ Configuración Avanzada

### Cambiar Formato de Video Output

Edita `add_multiple_media.lua`, línea ~210:

```lua
if info.extension == "mp4" then
    -- MP4 format (por defecto)
    local mp4_cfg = "bDRtcBAAAAA="
    reaper.GetSetProjectInfo_String(0, "RENDER_FORMAT", mp4_cfg, true)
end
```

### Ajustar Timeout para Videos Largos

Edita `add_multiple_media.lua`, línea ~220:

```lua
local timeout = 120  -- Cambiar a 180, 300, etc. para videos muy largos
```

### Configurar Audio del Video

En tu template de Reaper (`00 Voces.rpp`), configura:
- Efectos en el master
- Normalización
- EQ, compresión, etc.

Todo se aplicará automáticamente a los videos.

---

## 📝 Notas Importantes

### ⚠️ Espacio en Disco

Los videos ocupan espacio:
- Copia temporal en `Eleven\`
- Video original
- Video renderizado

**Recomendación:** Asegúrate de tener al menos **2x el tamaño** de todos tus videos en espacio libre.

### ⚠️ Tiempo de Procesamiento

Videos tardan más que audios:
- Video de 5 min puede tardar 1-2 minutos en renderizar
- Video de 30 min puede tardar 5-10 minutos
- Depende de la potencia de tu PC

**El timeout está configurado a 120 segundos por archivo.**

### ⚠️ Formatos Soportados

**Formatos de Video Probados:**
- ✅ MP4 (H.264, H.265)
- ✅ AVI
- ✅ MOV
- ✅ MKV

**Si usas otro formato:**
- El script detectará si es video por la extensión
- Reaper intentará importarlo
- Si falla, verás error en el log de Reaper

---

## 🎓 Casos de Uso

### 1. Serie de Clases Online

```python
Input:
- clase1.mp4  (15 min)
- clase2.mp4  (20 min)
- clase3.mp4  (18 min)

Output:
- Todos con audio profesional
- Normalizado -16 LUFS
- Sin ruido de fondo
- Listos para subir a plataforma
```

### 2. Podcast con Video

```python
Input:
- episodio_video.mp4  (podcast grabado en video)
- intro.mp3           (música intro)
- outro.mp3           (música outro)

Timeline Reaper:
|--- intro ---|--- episodio_video ---|--- outro ---|

Output:
- episodio_video_procesado.mp4 (con audio mejorado)
- intro_procesado.wav
- outro_procesado.wav
```

### 3. Webinar con Múltiples Segmentos

```python
Input:
- apertura.mp4
- presentacion.mp4
- qa.mp4
- cierre.mp4

Output:
- Todos procesados con audio consistente
- Mismo nivel de volumen
- Calidad broadcast
```

---

## 🔍 Verificar Resultados

### En Reaper (después del proceso)

1. Reaper permanece abierto
2. Puedes ver el timeline completo
3. Revisar forma de onda de cada archivo
4. Reproducir para verificar calidad
5. Re-renderizar si necesitas cambios

### En la Carpeta Procesados

```bash
# Verificar videos renderizados
cd "ruta\a\procesados"
dir *.mp4

# Verificar con FFprobe
ffprobe video_procesado.mp4

# Debe mostrar:
Stream #0:0: Video: h264 (original codec)
Stream #0:1: Audio: aac (procesado)
```

---

## 🚀 Performance Tips

### Para Muchos Videos

1. **Procesa en lotes pequeños** (3-5 videos a la vez)
2. **Cierra otras aplicaciones** para liberar RAM
3. **Usa SSD** para almacenamiento temporal
4. **Aumenta timeout** si tus videos son muy largos

### Para Videos 4K

1. **Asegúrate de tener suficiente RAM** (16GB+)
2. **El proceso puede ser más lento** pero preserva calidad
3. **Considera procesar de noche** para videos muy largos

---

## ✅ Resumen

AudioPro 1.8 ahora puede:

- 🎬 **Importar videos** directamente al timeline
- 🎵 **Mezclar videos y audios** en la misma sesión
- 📊 **Renderizar todo** desde un solo proyecto de Reaper
- 🔊 **Procesar audio** manteniendo video intacto
- 📁 **Organizar outputs** en carpeta procesados
- ⚡ **Automatizar completamente** el workflow

---

**AudioPro 1.8** 🎛️ - Video + Audio en un Solo Timeline

*"Procesa tus videos con calidad profesional de audio"*

