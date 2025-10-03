# 🎛️ AudioPro v1.7 - Guía Completa de Interfaces

## 🎉 ¡Ahora Tienes 2 Interfaces Disponibles!

AudioPro v1.7 ahora incluye **DOS formas diferentes** de usar la aplicación:

1. **🖼️ Interfaz Gráfica (GUI)** - Ventanas con botones (MÁS FÁCIL)
2. **💻 Interfaz de Terminal (CLI)** - Línea de comandos (MÁS POTENTE)

---

## 🖼️ INTERFAZ GRÁFICA (GUI) - ⭐ RECOMENDADA

### ✨ Características:

- ✅ **Ventanas intuitivas** con botones y menús visuales
- ✅ **Arrastrar y soltar** archivos (próximamente)
- ✅ **Sin comandos** - todo con clics del ratón
- ✅ **Log visual** en tiempo real del procesamiento
- ✅ **Barra de progreso** animada
- ✅ **Tema oscuro moderno** (fácil para la vista)
- ✅ **Multi-archivo** - agrega varios archivos a la vez
- ✅ **Google Drive** integrado

### 🚀 Cómo Usar la GUI:

#### **Opción 1: Desde el escritorio** (Más fácil)
1. Busca en tu escritorio: **"AudioPro GUI"**
2. Haz doble clic
3. ¡La ventana se abre automáticamente!

#### **Opción 2: Desde el Launcher**
1. Abre **"AudioPro v1.7"** desde el escritorio
2. Selecciona opción `1` (Interfaz Gráfica)
3. Presiona Enter

#### **Opción 3: Directamente**
1. Haz doble clic en `AudioPro_GUI.bat`

### 📖 Tutorial Paso a Paso (GUI):

```
┌─────────────────────────────────────────────────────────┐
│  🎛️ AudioPro v1.7                                      │
│  Procesamiento Profesional con Reaper                   │
├─────────────────────────────────────────────────────────┤
│  📁 Archivos a Procesar                                 │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐    │
│  │📄 Archivo│ │📂 Varios │ │🔗 Drive  │ │🗑️ Limpiar│    │
│  └─────────┘ └─────────┘ └─────────┘ └──────────┘    │
│  ┌─────────────────────────────────────────────────┐  │
│  │ • video1.mp4                                     │  │
│  │ • audio.wav                                      │  │
│  │ • Google Drive: https://...                      │  │
│  └─────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│  ⚙️ Configuración                                       │
│  ☑ ✨ Usar ElevenLabs Audio Isolation                 │
├─────────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────────┐ │
│  │   🎛️ PROCESAR CON REAPER                         │ │
│  └───────────────────────────────────────────────────┘ │
│  ▓▓▓▓▓▓▓▓░░░░░░░░░ Procesando...                      │
├─────────────────────────────────────────────────────────┤
│  📋 Log de Procesamiento                               │
│  ┌─────────────────────────────────────────────────┐  │
│  │ [14:32:10] 🎛️ Iniciando procesamiento...        │  │
│  │ [14:32:15] ✅ Agregado: video1.mp4              │  │
│  │ [14:32:20] 📊 Procesando 1/2                     │  │
│  │ [14:33:45] ✅ Completado: video1.mp4             │  │
│  └─────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 🎯 Flujo de Trabajo en la GUI:

**Paso 1: Agregar Archivos**
- Click en "📄 Agregar Archivo Local" para 1 archivo
- Click en "📂 Agregar Varios Archivos" para múltiples archivos
- Click en "🔗 Agregar desde Google Drive" para archivos de Drive

**Paso 2: Configurar**
- Marca/desmarca "✨ Usar ElevenLabs" según prefieras

**Paso 3: Procesar**
- Click en "🎛️ PROCESAR CON REAPER"
- ¡Espera y observa el progreso en tiempo real!

**Paso 4: Listo**
- Recibirás una notificación cuando termine
- Los archivos estarán en la carpeta de salida

### 💡 Ventajas de la GUI:

| Ventaja | Descripción |
|---------|-------------|
| **Visual** | Ves todo lo que pasa en tiempo real |
| **Intuitivo** | No necesitas saber comandos |
| **Multi-tarea** | Agrega varios archivos y procesa todos juntos |
| **Amigable** | Perfecto para principiantes |
| **Log claro** | Mensajes con colores y timestamps |

---

## 💻 INTERFAZ DE TERMINAL (CLI)

### ✨ Características:

- ✅ **Más rápida** que la GUI
- ✅ **Automatizable** con scripts
- ✅ **Procesamiento por lotes** desde archivos de texto
- ✅ **Ideal para workflows** repetitivos
- ✅ **Menos recursos** del sistema
- ✅ **Menú interactivo** también disponible

### 🚀 Cómo Usar la CLI:

#### **Opción 1: Desde el escritorio**
1. Busca: **"AudioPro CLI"**
2. Haz doble clic
3. Se abre la terminal con el menú

#### **Opción 2: Desde el Launcher**
1. Abre **"AudioPro v1.7"** desde el escritorio
2. Selecciona opción `2` (Terminal CLI)
3. Presiona Enter

#### **Opción 3: Comandos directos**
```bash
# Procesar 1 archivo
python audiopro_cli.py -f "C:\Videos\video.mp4"

# Procesar desde Drive
python audiopro_cli.py -d "https://drive.google.com/file/d/XXXXX"

# Procesar lote
python audiopro_cli.py -b "archivos.txt"
```

### 💡 Ventajas de la CLI:

| Ventaja | Descripción |
|---------|-------------|
| **Velocidad** | Más rápida, menos overhead |
| **Automatización** | Integrable en scripts |
| **Lotes** | Procesa muchos archivos fácilmente |
| **Scripting** | Ideal para workflows complejos |
| **Remoto** | Funciona sin GUI/escritorio |

---

## 🆚 GUI vs CLI - ¿Cuál Elegir?

### **Elige la GUI si:**
- ✅ Eres principiante
- ✅ Procesas archivos ocasionalmente
- ✅ Prefieres ver todo visualmente
- ✅ Quieres algo simple y directo
- ✅ No te gustan las terminales

### **Elige la CLI si:**
- ✅ Eres usuario avanzado
- ✅ Procesas muchos archivos regularmente
- ✅ Quieres automatizar el proceso
- ✅ Necesitas integrar con otros scripts
- ✅ Te sientes cómodo con terminales

---

## 📂 Accesos Directos Disponibles

En tu escritorio ahora tienes **3 accesos directos**:

### 1. **"AudioPro v1.7"** 🎛️
- **Launcher/Selector** - Te pregunta qué interfaz quieres usar
- **Recomendado para:** Cuando no estás seguro cuál usar

### 2. **"AudioPro GUI"** 🖼️
- **Interfaz Gráfica** directa
- **Recomendado para:** Uso diario, principiantes

### 3. **"AudioPro CLI"** 💻
- **Terminal** directa
- **Recomendado para:** Usuarios avanzados, automatización

---

## 🎯 Ejemplos de Uso por Escenario

### **Escenario 1: Procesar 1 video rápidamente**
**Método más fácil:** GUI
1. Doble clic en "AudioPro GUI"
2. Click "📄 Agregar Archivo Local"
3. Selecciona tu video
4. Click "🎛️ PROCESAR"

### **Escenario 2: Procesar 50 videos de una carpeta**
**Método más eficiente:** CLI con lote
1. Crea `videos.txt` con todas las rutas
2. Ejecuta: `python audiopro_cli.py -b videos.txt`
3. ¡Déjalo corriendo y listo!

### **Escenario 3: Procesar archivos de Drive**
**Ambos métodos funcionan bien:**
- **GUI:** Click "🔗 Google Drive", pega URL
- **CLI:** `python audiopro_cli.py -d "URL"`

### **Escenario 4: Automatizar procesamiento diario**
**Mejor opción:** CLI con script
```bash
# script_diario.bat
for %%f in (C:\Grabaciones\*.mp4) do (
    python audiopro_cli.py -f "%%f"
)
```

---

## 🛠️ Configuración Común (Ambas Interfaces)

### **ElevenLabs API Key:**

**Para GUI y CLI:**
1. Abre `AudioPro_GUI.bat` o `AudioPro_CLI.bat` con un editor
2. Busca esta línea:
   ```batch
   REM set ELEVENLABS_API_KEY=tu_api_key_aqui
   ```
3. Elimina `REM ` y pon tu API key:
   ```batch
   set ELEVENLABS_API_KEY=sk-XXXXXXXXXXXXX
   ```
4. Guarda el archivo

**O establece variable de entorno global:**
```powershell
# PowerShell
$env:ELEVENLABS_API_KEY = "sk-XXXXXXXXXXXXX"
```

---

## 📊 Comparación Detallada

| Característica | GUI 🖼️ | CLI 💻 |
|----------------|---------|--------|
| **Facilidad de uso** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Velocidad** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Automatización** | ❌ | ⭐⭐⭐⭐⭐ |
| **Visual feedback** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Multi-archivo** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Recursos sistema** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Curva aprendizaje** | Baja | Media |
| **Ideal para** | Principiantes | Avanzados |

---

## 🎉 ¡Empieza Ahora!

### **Para Principiantes:**
1. Ve a tu escritorio
2. Doble clic en **"AudioPro GUI"**
3. ¡Explora la interfaz!

### **Para Usuarios Avanzados:**
1. Ve a tu escritorio
2. Doble clic en **"AudioPro CLI"**
3. Prueba el menú interactivo primero

### **Si no estás seguro:**
1. Abre **"AudioPro v1.7"**
2. Te dejará elegir
3. ¡Prueba ambas y decide!

---

## 📚 Documentación Adicional

- **`GUIA_RAPIDA.md`** - Tutorial rápido CLI
- **`README_CLI.md`** - Documentación completa CLI
- **`COMO_USAR.txt`** - Referencia rápida
- **Este archivo** - Comparación GUI vs CLI

---

**AudioPro v1.7** - Procesamiento Profesional de Audio/Video 🎛️

*Ahora con interfaz gráfica intuitiva Y terminal potente - ¡Tú eliges!*

