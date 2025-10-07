# 🚀 Guía Rápida - AudioPro CLI v1.7

## ⚡ Inicio Rápido (3 pasos)

### **Paso 1: Abre PowerShell o CMD**
```bash
cd "D:\CURSOR\Audiopro 1.7"
```

### **Paso 2: Ejecuta la app**
```bash
python audiopro_cli.py
```

### **Paso 3: Sigue el menú interactivo**
¡Listo! La app te guiará paso a paso.

---

## 📖 Métodos de Uso

### 🎯 **MÉTODO 1: Modo Interactivo (RECOMENDADO para principiantes)**

**Windows (doble clic):**
- Ejecuta `start_cli.bat` o `EJEMPLO_USO.bat`

**O desde terminal:**
```bash
python audiopro_cli.py
```

**Verás esto:**
```
============================================================
   🎛️  AudioPro CLI v1.7 - Reaper Edition
============================================================

MENÚ PRINCIPAL
1. Procesar archivo desde ruta local
2. Procesar archivo desde Google Drive  
3. Procesar lote desde archivo de texto
4. Configuración
5. Salir

Selecciona una opción: _
```

---

### 🎮 **MÉTODO 2: Comandos Directos**

#### **Procesar 1 archivo local:**
```bash
python audiopro_cli.py -f "C:\Videos\video.mp4"
```

#### **Procesar desde Google Drive:**
```bash
python audiopro_cli.py -d "https://drive.google.com/file/d/1ABC123/view"
```

#### **Procesar VARIOS archivos:**
```bash
python audiopro_cli.py -b "archivos_prueba.txt"
```

#### **Sin ElevenLabs:**
```bash
python audiopro_cli.py -f "video.mp4" --no-elevenlabs
```

---

## 📝 **MÉTODO 3: Procesamiento por Lotes**

### **Paso 1: Crea un archivo de texto**
Crea `mis_videos.txt` con este contenido:
```text
C:\Videos\video1.mp4
C:\Videos\video2.mp4
C:\Audio\podcast.wav
https://drive.google.com/file/d/1ABC123/view
```

### **Paso 2: Procesa todos los archivos**
```bash
python audiopro_cli.py -b "mis_videos.txt"
```

La app procesará **todos** los archivos automáticamente, uno por uno.

---

## ⚙️ Configuración de ElevenLabs (Opcional)

Si quieres usar ElevenLabs Audio Isolation:

### **Windows PowerShell:**
```powershell
$env:ELEVENLABS_API_KEY = "tu_api_key_aqui"
```

### **Windows CMD:**
```cmd
set ELEVENLABS_API_KEY=tu_api_key_aqui
```

### **O edita `start_cli.bat`:**
Abre `start_cli.bat` y descomenta estas líneas:
```batch
set ELEVENLABS_API_KEY=tu_api_key_aqui
set ELEVENLABS_BASE_URL=https://api.elevenlabs.io
```

---

## 📂 ¿Dónde se guardan los archivos procesados?

### **Archivos locales:**
```
[carpeta_original]/procesados/archivo_procesado.mp4
```

**Ejemplo:**
- Original: `C:\Videos\video.mp4`
- Procesado: `C:\Videos\procesados\video_procesado.mp4`

### **Archivos de Drive:**
```
F:\00\00 Reaper\Procesados\[sesion]\archivo_procesado.mp4
```

### **Sesiones de Reaper:**
```
F:\00\00 Reaper\Procesados\[sesion]\[sesion].rpp
```

---

## 🎯 Ejemplos Prácticos

### **Ejemplo 1: Video de YouTube descargado**
```bash
python audiopro_cli.py -f "C:\Descargas\video_youtube.mp4"
```

### **Ejemplo 2: Múltiples podcasts**
Crea `podcasts.txt`:
```text
C:\Podcasts\episodio1.mp3
C:\Podcasts\episodio2.mp3
C:\Podcasts\episodio3.mp3
```

Ejecuta:
```bash
python audiopro_cli.py -b "podcasts.txt"
```

### **Ejemplo 3: Archivos de Drive sin ElevenLabs**
```bash
python audiopro_cli.py -d "https://drive.google.com/file/d/1ABC123/view" --no-elevenlabs
```

---

## ❓ ¿Qué hace la app?

1. ✅ **Extrae el audio** del archivo (video o audio)
2. ✅ **Aplica ElevenLabs** Audio Isolation (opcional - limpia la voz)
3. ✅ **Carga en Reaper** con tu template profesional
4. ✅ **Procesa con plugins** (Waves, etc.)
5. ✅ **Renderiza** automáticamente
6. ✅ **Combina con video** si es necesario
7. ✅ **Guarda** el resultado final

---

## 🔥 Tips y Trucos

### **Tip 1: Ver ayuda completa**
```bash
python audiopro_cli.py --help
```

### **Tip 2: Procesar carpeta completa (PowerShell)**
```powershell
Get-ChildItem "C:\Videos\*.mp4" | ForEach-Object {
    python audiopro_cli.py -f $_.FullName
}
```

### **Tip 3: Procesar carpeta completa (Batch)**
```batch
for %%f in (C:\Videos\*.mp4) do python audiopro_cli.py -f "%%f"
```

### **Tip 4: Ver configuración actual**
Ejecuta la app en modo interactivo y selecciona opción `4` (Configuración)

---

## 🆘 Solución de Problemas

### ❌ "Python no reconocido"
**Solución:** Instala Python y agrégalo al PATH del sistema

### ❌ "FFmpeg no encontrado"
**Solución:** Instala FFmpeg y agrégalo al PATH

### ❌ "Reaper no abre"
**Solución:** Verifica la ruta de Reaper en `audiopro_cli.py` línea 32

### ❌ "API key no configurada"
**Solución:** Configura `ELEVENLABS_API_KEY` o usa `--no-elevenlabs`

### ❌ "Timeout en render"
**Solución:** El procesamiento puede tardar. Verifica que Reaper esté renderizando correctamente.

---

## 🎉 ¡Empieza Ahora!

**La forma más fácil de empezar:**

1. Abre terminal en `D:\CURSOR\Audiopro 1.7`
2. Ejecuta: `python audiopro_cli.py`
3. Selecciona opción `1`
4. Ingresa la ruta de tu archivo
5. ¡Disfruta del procesamiento automático!

---

**¿Dudas?** Revisa `README_CLI.md` para documentación completa.

