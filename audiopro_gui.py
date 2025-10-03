"""
AudioPro GUI v1.7 - Interfaz Gráfica
Aplicación con ventanas intuitivas para procesamiento profesional con Reaper
"""

import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from datetime import datetime
import queue

# Importar funciones del CLI
from audio_utils_cli import get_bytes_from_drive

# Configuración
REAPER_EXE = r"C:\Program Files\REAPER (x64)\reaper.exe"
REAPER_TEMPLATE = r"F:\00\00 Reaper\00 Voces.rpp"
REAPER_SESSIONS_DIR = r"F:\00\00 Reaper\Procesados"

# ElevenLabs
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_BASE_URL = os.getenv("ELEVENLABS_BASE_URL", "https://api.elevenlabs.io")


class AudioProGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AudioPro v1.7 - Reaper Edition")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # Variables
        self.files_queue = []
        self.processing = False
        self.use_elevenlabs = tk.BooleanVar(value=bool(ELEVENLABS_API_KEY))

        # Cola para mensajes entre threads
        self.message_queue = queue.Queue()

        # Configurar estilo
        self.setup_style()

        # Crear interfaz
        self.create_widgets()

        # Iniciar verificación de mensajes
        self.check_messages()

    def setup_style(self):
        """Configura el estilo visual moderno con fuente Roobert y colores de Platzi."""
        style = ttk.Style()
        style.theme_use('clam')

        # Colores de Platzi - Modernos
        platzi_dark = "#0c1526"      # Azul muy oscuro (más moderno)
        platzi_dark_2 = "#121f3d"    # Azul oscuro medio
        platzi_green = "#98ca3f"     # Verde característico de Platzi
        platzi_green_hover = "#b8e65f"  # Verde claro hover
        platzi_blue = "#24385b"      # Azul medio
        platzi_blue_light = "#2e4a6d"  # Azul más claro para hover
        platzi_white = "#ffffff"     # Blanco
        platzi_gray = "#a6b6cc"      # Gris claro
        platzi_gray_dark = "#6b7a99"  # Gris más oscuro (para futuro uso)

        # Fuente principal (Segoe UI funciona en Windows, con look moderno)
        # Si tienes Roobert instalada, cámbiala manualmente por 'Roobert'
        font_family = 'Segoe UI'
        # Prevenir warning de variable no usada
        _ = platzi_gray_dark

        # Configurar estilos modernos
        style.configure('TFrame', background=platzi_dark)
        style.configure('Card.TFrame', background=platzi_dark_2, relief='flat')

        # Labels con Roobert
        style.configure('TLabel', background=platzi_dark, foreground=platzi_white,
                        font=(font_family, 10))
        style.configure('Title.TLabel', font=(font_family, 24, 'bold'),
                        foreground=platzi_green, background=platzi_dark)
        style.configure('Subtitle.TLabel', font=(font_family, 12),
                        foreground=platzi_gray, background=platzi_dark)
        style.configure('SectionTitle.TLabel', font=(font_family, 11, 'bold'),
                        foreground=platzi_white, background=platzi_dark_2)

        # Botones modernos con Roobert
        style.configure('TButton', font=(font_family, 10, 'bold'), padding=(15, 10),
                        background=platzi_blue, foreground=platzi_white,
                        borderwidth=0, relief='flat')
        style.configure('Accent.TButton', font=(font_family, 12, 'bold'),
                        padding=(20, 12), background=platzi_green,
                        foreground=platzi_dark, borderwidth=0, relief='flat')
        style.configure('Secondary.TButton', font=(font_family, 9),
                        padding=(12, 8), background=platzi_blue,
                        foreground=platzi_white, borderwidth=0)

        # Checkbox moderno
        style.configure('TCheckbutton', background=platzi_dark_2,
                        foreground=platzi_white, font=(font_family, 10))

        # Barra de progreso moderna
        style.configure('TProgressbar', background=platzi_green,
                        troughcolor=platzi_blue, borderwidth=0,
                        thickness=8)

        # LabelFrame moderno
        style.configure('TLabelframe', background=platzi_dark_2,
                        borderwidth=0, relief='flat')
        style.configure('TLabelframe.Label', background=platzi_dark_2,
                        foreground=platzi_white, font=(font_family, 11, 'bold'))

        # Mapear estados de los botones con transiciones suaves
        style.map('Accent.TButton',
                  background=[('active', platzi_green_hover),
                              ('pressed', '#88ba2f')],
                  foreground=[('active', platzi_dark)])

        style.map('TButton',
                  background=[('active', platzi_blue_light),
                              ('pressed', platzi_blue)],
                  foreground=[('active', platzi_white)])

        style.map('Secondary.TButton',
                  background=[('active', platzi_blue_light)])

        self.root.configure(bg=platzi_dark)

    def create_widgets(self):
        """Crea todos los widgets de la interfaz."""
        # Frame principal con padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))

        title = ttk.Label(header_frame, text="🎛️ AudioPro v1.7",
                          style='Title.TLabel')
        title.grid(row=0, column=0, sticky=tk.W)

        subtitle = ttk.Label(header_frame,
                             text="Procesamiento Profesional con Reaper",
                             style='Subtitle.TLabel')
        subtitle.grid(row=1, column=0, sticky=tk.W)

        # Separador
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=1, column=0, sticky=(tk.W, tk.E), pady=10)

        # Sección de archivos
        files_frame = ttk.LabelFrame(main_frame, text="📁 Archivos a Procesar",
                                     padding="10")
        files_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        files_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Botones de agregar archivos
        buttons_frame = ttk.Frame(files_frame)
        buttons_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        btn_add_file = ttk.Button(buttons_frame, text="📄 Agregar Archivo Local",
                                  command=self.add_file, style='Accent.TButton')
        btn_add_file.grid(row=0, column=0, padx=5)

        btn_add_files = ttk.Button(buttons_frame, text="📂 Agregar Varios Archivos",
                                   command=self.add_multiple_files)
        btn_add_files.grid(row=0, column=1, padx=5)

        btn_add_drive = ttk.Button(buttons_frame, text="🔗 Agregar desde Google Drive",
                                   command=self.add_from_drive)
        btn_add_drive.grid(row=0, column=2, padx=5)

        btn_clear = ttk.Button(buttons_frame, text="🗑️ Limpiar Lista",
                               command=self.clear_files)
        btn_clear.grid(row=0, column=3, padx=5)

        # Lista de archivos
        list_frame = ttk.Frame(files_frame)
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        files_frame.rowconfigure(1, weight=1)

        self.files_listbox = tk.Listbox(list_frame, height=8,
                                        font=('Segoe UI', 10),
                                        bg="#24385b", fg="#ffffff",
                                        selectbackground="#98ca3f",
                                        selectforeground="#0c1526",
                                        highlightthickness=0,
                                        borderwidth=0,
                                        activestyle='none',
                                        relief='flat')
        self.files_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical",
                                  command=self.files_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.files_listbox.configure(yscrollcommand=scrollbar.set)

        # Configuración
        config_frame = ttk.LabelFrame(main_frame, text="⚙️ Configuración", padding="10")
        config_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=10)

        self.elevenlabs_check = ttk.Checkbutton(
            config_frame,
            text="✨ Usar ElevenLabs Audio Isolation",
            variable=self.use_elevenlabs)
        self.elevenlabs_check.grid(row=0, column=0, sticky=tk.W, pady=5)

        if not ELEVENLABS_API_KEY:
            self.elevenlabs_check.configure(state='disabled')
            ttk.Label(config_frame, text="⚠️ API Key no configurada",
                      foreground="#ff9800").grid(row=0, column=1, padx=10)

        # Botón de procesamiento
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=10)

        self.process_btn = ttk.Button(btn_frame, text="🎛️ PROCESAR CON REAPER",
                                      command=self.start_processing,
                                      style='Accent.TButton')
        self.process_btn.grid(row=0, column=0, sticky=(tk.W, tk.E))
        btn_frame.columnconfigure(0, weight=1)

        # Barra de progreso
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        # Log de salida
        log_frame = ttk.LabelFrame(main_frame, text="📋 Log de Procesamiento",
                                   padding="10")
        log_frame.grid(row=6, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=10,
                                                  font=('Consolas', 10),
                                                  bg="#24385b", fg="#98ca3f",
                                                  wrap=tk.WORD,
                                                  highlightthickness=0,
                                                  borderwidth=0,
                                                  insertbackground="#98ca3f",
                                                  relief='flat',
                                                  padx=10, pady=10)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Footer
        footer = ttk.Label(main_frame,
                           text="AudioPro v1.7 🎛️ | Procesamiento Profesional",
                           style='Subtitle.TLabel')
        footer.grid(row=7, column=0, pady=(10, 0))

    def log(self, message, color=None):
        """Agrega un mensaje al log."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"

        self.log_text.insert(tk.END, formatted_message)
        if color:
            # Aplicar color al último mensaje
            start_line = self.log_text.index("end-2c linestart")
            end_line = self.log_text.index("end-1c")
            tag_name = f"color_{color}"
            self.log_text.tag_config(tag_name, foreground=color)
            self.log_text.tag_add(tag_name, start_line, end_line)

        self.log_text.see(tk.END)
        self.log_text.update()

    def add_file(self):
        """Agregar un archivo local."""
        filetypes = (
            ('Archivos de Audio/Video',
             '*.mp4 *.mp3 *.wav *.avi *.mov *.mkv *.m4a *.flac'),
            ('Todos los archivos', '*.*')
        )

        filename = filedialog.askopenfilename(title="Seleccionar archivo",
                                              filetypes=filetypes)

        if filename:
            self.files_queue.append(('local', filename))
            self.files_listbox.insert(tk.END, f"📄 {os.path.basename(filename)}")
            self.log(f"✅ Agregado: {os.path.basename(filename)}", "#00ff00")

    def add_multiple_files(self):
        """Agregar múltiples archivos locales."""
        filetypes = (
            ('Archivos de Audio/Video',
             '*.mp4 *.mp3 *.wav *.avi *.mov *.mkv *.m4a *.flac'),
            ('Todos los archivos', '*.*')
        )

        filenames = filedialog.askopenfilenames(title="Seleccionar archivos",
                                                filetypes=filetypes)

        for filename in filenames:
            self.files_queue.append(('local', filename))
            self.files_listbox.insert(tk.END, f"📄 {os.path.basename(filename)}")

        if filenames:
            self.log(f"✅ Agregados {len(filenames)} archivo(s)", "#00ff00")

    def add_from_drive(self):
        """Agregar archivo desde Google Drive."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Agregar desde Google Drive")
        dialog.geometry("550x220")
        dialog.configure(bg="#0c1526")
        dialog.resizable(False, False)

        ttk.Label(dialog, text="Pega la URL de Google Drive:").pack(pady=20)

        url_entry = ttk.Entry(dialog, width=60)
        url_entry.pack(pady=10)
        url_entry.focus()

        def add_url():
            url = url_entry.get().strip()
            if url:
                self.files_queue.append(('drive', url))
                self.files_listbox.insert(tk.END, f"🔗 Google Drive: {url[:50]}...")
                self.log("✅ Agregado desde Drive", "#00ff00")
                dialog.destroy()
            else:
                messagebox.showwarning("Advertencia",
                                       "Por favor ingresa una URL válida")

        ttk.Button(dialog, text="Agregar", command=add_url).pack(pady=10)

    def clear_files(self):
        """Limpiar la lista de archivos."""
        self.files_queue.clear()
        self.files_listbox.delete(0, tk.END)
        self.log("🗑️ Lista limpiada", "#ffff00")

    def start_processing(self):
        """Inicia el procesamiento en un thread separado."""
        if not self.files_queue:
            messagebox.showwarning("Advertencia",
                                   "No hay archivos para procesar.\nAgrega archivos primero.")
            return

        if self.processing:
            messagebox.showinfo("Información", "Ya hay un procesamiento en curso.")
            return

        # Deshabilitar botón y mostrar progreso
        self.process_btn.configure(state='disabled')
        self.progress.start()
        self.processing = True

        # Iniciar procesamiento en thread
        thread = threading.Thread(target=self.process_files, daemon=True)
        thread.start()

    def process_files(self):
        """Procesa todos los archivos en la cola - NUEVO: procesamiento por lotes."""
        total = len(self.files_queue)

        self.message_queue.put(('log',
                                f"🎛️ Iniciando procesamiento por lotes de {total} archivo(s)...",
                                "#00d4ff"))

        # Fase 1: Preparar todos los archivos
        prepared_files = []

        for idx, (file_type, file_path) in enumerate(self.files_queue, 1):
            self.message_queue.put(('log', "\n" + "=" * 60, None))
            self.message_queue.put(('log', f"📊 Preparando {idx}/{total}", "#00d4ff"))
            self.message_queue.put(('log', "=" * 60, None))

            try:
                if file_type == 'local':
                    result = self.prepare_local_file(file_path)
                elif file_type == 'drive':
                    result = self.prepare_drive_file(file_path)

                if result:
                    prepared_files.append(result)
                    self.message_queue.put(('log', f"✅ Preparado: {result['display_name']}", "#00ff00"))
                else:
                    self.message_queue.put(('log', "❌ Error preparando archivo", "#ff0000"))

            except Exception as e:
                self.message_queue.put(('log', f"❌ Error: {str(e)}", "#ff0000"))

        # Fase 2: Procesar todos juntos en Reaper
        if prepared_files:
            self.message_queue.put(('log', "\n" + "=" * 60, None))
            self.message_queue.put(('log', f"🎛️ Procesando {len(prepared_files)} archivo(s) en Reaper...", "#00d4ff"))
            self.message_queue.put(('log', "=" * 60 + "\n", None))

            try:
                self.process_batch_with_reaper(prepared_files)
                self.message_queue.put(('log', "\n🎉 Procesamiento completado exitosamente!", "#00ff00"))
            except Exception as e:
                self.message_queue.put(('log', f"\n❌ Error en procesamiento Reaper: {str(e)}", "#ff0000"))
        else:
            self.message_queue.put(('log', "\n❌ No se pudo preparar ningún archivo", "#ff0000"))

        self.message_queue.put(('done', None, None))

    def prepare_local_file(self, file_path):
        """Prepara un archivo local para procesamiento por lotes."""
        from audio_utils_cli import (extract_audio_wav16_mono, 
                                     process_audio_with_elevenlabs,
                                     is_audio_only_file)

        self.message_queue.put(('log', f"📁 Archivo: {os.path.basename(file_path)}", None))

        # Determinar nombre base sin extensión
        file_name = os.path.basename(file_path)
        original_name = os.path.splitext(file_name)[0]
        source_dir = os.path.dirname(file_path)
        
        # Detectar si es video o audio puro
        is_audio = is_audio_only_file(file_path)
        
        if is_audio:
            self.message_queue.put(('log', "🎵 Archivo de audio detectado", None))
        else:
            self.message_queue.put(('log', "🎬 Video detectado - extrayendo audio en calidad 48kHz 24-bit", None))

        # Extraer audio (48kHz 24-bit para mantener calidad)
        self.message_queue.put(('log', "🎵 Extrayendo audio...", None))
        extracted_wav_path = extract_audio_wav16_mono(file_path, bit_depth=24)

        # ElevenLabs si está habilitado
        if self.use_elevenlabs.get() and ELEVENLABS_API_KEY:
            self.message_queue.put(('log', "✨ Procesando con ElevenLabs...", None))
            # Leer el WAV extraído
            with open(extracted_wav_path, 'rb') as f:
                audio_bytes = f.read()
            # Procesar con ElevenLabs
            processed_bytes = process_audio_with_elevenlabs(audio_bytes, ELEVENLABS_API_KEY, ELEVENLABS_BASE_URL)
            # Sobrescribir el archivo con el procesado
            with open(extracted_wav_path, 'wb') as f:
                f.write(processed_bytes)

        return {
            'temp_path': extracted_wav_path,
            'original_name': original_name,
            'source_dir': source_dir or REAPER_SESSIONS_DIR,
            'display_name': file_name,
            'is_video': not is_audio,
            'original_file': file_path  # Guardar ruta original para videos
        }

    def prepare_drive_file(self, drive_url):
        """Prepara un archivo de Google Drive para procesamiento por lotes."""
        from audio_utils_cli import (extract_audio_wav16_mono, 
                                     process_audio_with_elevenlabs,
                                     is_audio_only_file)
        import tempfile

        self.message_queue.put(('log', "🔗 Descargando desde Google Drive...", None))

        result = get_bytes_from_drive(drive_url)
        if not result:
            raise Exception("No se pudo descargar desde Drive")

        file_bytes, file_name = result

        # Determinar nombre base
        original_name = os.path.splitext(file_name)[0]

        # Guardar el archivo descargado temporalmente
        temp_input = tempfile.NamedTemporaryFile(suffix=os.path.splitext(file_name)[1], delete=False)
        temp_input.write(file_bytes)
        temp_input.close()
        
        # Detectar si es video o audio puro
        is_audio = is_audio_only_file(temp_input.name)
        
        if is_audio:
            self.message_queue.put(('log', "🎵 Archivo de audio detectado", None))
        else:
            self.message_queue.put(('log', "🎬 Video detectado - extrayendo audio en calidad 48kHz 24-bit", None))

        # Extraer audio (48kHz 24-bit para mantener calidad)
        self.message_queue.put(('log', "🎵 Extrayendo audio...", None))
        extracted_wav_path = extract_audio_wav16_mono(temp_input.name, bit_depth=24)

        # ElevenLabs si está habilitado
        if self.use_elevenlabs.get() and ELEVENLABS_API_KEY:
            self.message_queue.put(('log', "✨ Procesando con ElevenLabs...", None))
            # Leer el WAV extraído
            with open(extracted_wav_path, 'rb') as f:
                audio_bytes = f.read()
            # Procesar con ElevenLabs
            processed_bytes = process_audio_with_elevenlabs(audio_bytes, ELEVENLABS_API_KEY, ELEVENLABS_BASE_URL)
            # Sobrescribir el archivo con el procesado
            with open(extracted_wav_path, 'wb') as f:
                f.write(processed_bytes)

        return {
            'temp_path': extracted_wav_path,
            'original_name': original_name,
            'source_dir': REAPER_SESSIONS_DIR,
            'display_name': file_name,
            'is_video': not is_audio,
            'original_file': temp_input.name  # Guardar ruta temporal para videos
        }

    def process_batch_with_reaper(self, prepared_files):
        """Procesa múltiples archivos en Reaper usando el nuevo script de batch."""
        import subprocess
        import time

        if not prepared_files:
            raise Exception("No hay archivos preparados para procesar")

        # Usar el directorio del primer archivo como base
        base_dir = prepared_files[0]['source_dir']

        # Crear nombre de sesión
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_name = os.path.join(base_dir, f"AudioPro_Batch_{timestamp}.rpp")

        # Preparar listas separadas por "|"
        audio_files_list = "|".join([f['temp_path'] for f in prepared_files])
        output_names_list = "|".join([f['original_name'] for f in prepared_files])

        self.message_queue.put(('log', f"📝 Sesión: {os.path.basename(session_name)}", None))
        self.message_queue.put(('log', f"📂 Directorio: {base_dir}", None))
        self.message_queue.put(('log', f"🎬 Insertando {len(prepared_files)} archivo(s) en timeline...", None))

        # Configurar parámetros para el script Lua
        subprocess.run([
            REAPER_EXE,
            "-setextstate", "AudioPro", "session_name", session_name,
            "-setextstate", "AudioPro", "template_path", REAPER_TEMPLATE,
            "-setextstate", "AudioPro", "audio_files_list", audio_files_list,
            "-setextstate", "AudioPro", "output_names_list", output_names_list,
            "-setextstate", "AudioPro", "session_dir", base_dir,
            "-nonewinst"
        ], check=True, capture_output=True)

        # Ejecutar el script de batch
        script_path = os.path.join(os.path.dirname(__file__), "add_multiple_audios.lua")

        self.message_queue.put(('log', "🎛️ Ejecutando Reaper...", None))

        subprocess.run([
            REAPER_EXE,
            "-nonewinst",
            "-nosplash",
            "-script", script_path
        ], check=True, capture_output=True)

        # Esperar un poco para que Reaper termine
        time.sleep(5)

        # Verificar archivos de salida
        procesados_dir = os.path.join(base_dir, "procesados")
        
        # Post-procesar: Re-embeber audio en videos
        from audio_utils_cli import remux_video_with_audio
        
        for file_info in prepared_files:
            if file_info.get('is_video', False):
                self.message_queue.put(('log', f"\n🎬 Re-embebiendo audio en video: {file_info['display_name']}", "#00d4ff"))
                
                # Ruta del audio procesado por Reaper
                processed_audio = os.path.join(procesados_dir, f"{file_info['original_name']}_procesado.wav")
                
                # Ruta del video original
                original_video = file_info['original_file']
                
                # Determinar extensión del video original
                original_ext = os.path.splitext(file_info['display_name'])[1]
                
                # Ruta del video final con audio embebido
                final_video = os.path.join(procesados_dir, f"{file_info['original_name']}_procesado{original_ext}")
                
                try:
                    if os.path.exists(processed_audio):
                        remux_video_with_audio(original_video, processed_audio, final_video)
                        self.message_queue.put(('log', f"✅ Video con audio procesado: {os.path.basename(final_video)}", "#00ff00"))
                        
                        # Eliminar el WAV temporal (ya está embebido en el video)
                        try:
                            os.unlink(processed_audio)
                        except Exception:
                            pass
                    else:
                        self.message_queue.put(('log', f"⚠️ No se encontró audio procesado para: {file_info['display_name']}", "#ffff00"))
                except Exception as e:
                    self.message_queue.put(('log', f"❌ Error re-embebiendo video: {str(e)}", "#ff0000"))

        self.message_queue.put(('log', "\n✅ Procesamiento completado", "#00ff00"))
        self.message_queue.put(('log', f"📂 Archivos guardados en: {procesados_dir}", "#00ff00"))

        # Limpiar archivos temporales
        for f in prepared_files:
            try:
                os.unlink(f['temp_path'])
            except Exception:
                pass
            
            # Limpiar archivo temporal de Drive
            if f.get('is_video') and 'drive' in f.get('original_file', '').lower():
                try:
                    os.unlink(f['original_file'])
                except Exception:
                    pass

        return {'output_dir': procesados_dir}

    def check_messages(self):
        """Verifica mensajes de otros threads."""
        try:
            while True:
                msg_type, message, color = self.message_queue.get_nowait()

                if msg_type == 'log':
                    self.log(message, color)
                elif msg_type == 'done':
                    self.progress.stop()
                    self.process_btn.configure(state='normal')
                    self.processing = False
                    messagebox.showinfo("Completado",
                                        "Procesamiento finalizado exitosamente!")

        except queue.Empty:
            pass

        # Verificar nuevamente en 100ms
        self.root.after(100, self.check_messages)


def main():
    """Función principal."""
    root = tk.Tk()
    AudioProGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
