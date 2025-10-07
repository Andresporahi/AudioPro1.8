"""
AudioPro CLI v1.7 - Aplicación de línea de comandos
Procesamiento profesional con Reaper sin interfaz Streamlit
"""

import os
import tempfile
import subprocess
import shutil
import time
import argparse
from datetime import datetime
from typing import Optional
from colorama import Fore, Style, init
from audio_utils_cli import (
    get_bytes_from_local_path,
    get_bytes_from_drive,
    extract_audio_wav16_mono,
    run_ffmpeg,
    is_audio_only_file,
    process_audio_with_elevenlabs,
    print_info,
    print_success,
    print_warning,
    print_error
)

# Inicializar colorama
init(autoreset=True)

# Configuración
REAPER_EXE = r"C:\Program Files\REAPER (x64)\reaper.exe"
REAPER_TEMPLATE = r"F:\00\00 Reaper\00 Voces.rpp"
REAPER_SESSIONS_DIR = r"F:\00\00 Reaper\Procesados"

# ElevenLabs - Cargar desde variables de entorno
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_BASE_URL = os.getenv("ELEVENLABS_BASE_URL", "https://api.elevenlabs.io")


def print_banner():
    """Imprime el banner de la aplicación."""
    print(f"\n{Fore.CYAN}{'=' * 60}")
    print(f"{Fore.CYAN}   🎛️  AudioPro CLI v1.7 - Reaper Edition")
    print(f"{Fore.CYAN}   Procesamiento Profesional de Audio/Video")
    print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")


def add_audio_to_reaper_session(session_path: str, audio_file: str, original_name: str = None):
    """Agrega un archivo de audio a una sesión de Reaper usando ReaScript Lua.

    Args:
        session_path: Ruta al archivo .rpp de la sesión
        audio_file: Ruta al archivo de audio a agregar
        original_name: Nombre original del archivo (sin extensión)
    """
    # Usar el script Lua estático
    lua_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "add_audio_to_session.lua"))
    if not os.path.exists(lua_script):
        print_error("Script Lua no encontrado: add_audio_to_session.lua")
        return

    # Crear script temporal que establece ExtState y ejecuta el script principal
    temp_script = tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.lua',
        delete=False,
        encoding='utf-8'
    )

    # Convertir rutas a formato compatible con Lua (usar / en lugar de \)
    lua_script_path = lua_script.replace('\\', '/')
    audio_file_path = audio_file.replace('\\', '/')
    session_path_path = session_path.replace('\\', '/')
    template_path = REAPER_TEMPLATE.replace('\\', '/')

    # Usar el nombre original proporcionado o fallback al nombre del audio_file
    if not original_name:
        original_name = os.path.splitext(os.path.basename(audio_file))[0]

    temp_script.write(f"""
-- Script temporal para pasar parámetros usando ExtState
-- Según documentación de ReaScript: https://www.reaper.fm/sdk/reascript/reascript.php

-- Establecer parámetros usando ExtState
reaper.SetExtState("AudioPro", "audio_file", [[{audio_file_path}]], false)
reaper.SetExtState("AudioPro", "session_name", [[{session_path_path}]], false)
reaper.SetExtState("AudioPro", "template_path", [[{template_path}]], false)
reaper.SetExtState("AudioPro", "original_name", [[{original_name}]], false)

-- Ejecutar el script principal
dofile([[{lua_script_path}]])

-- Limpiar ExtState
reaper.DeleteExtState("AudioPro", "audio_file", false)
reaper.DeleteExtState("AudioPro", "session_name", false)
reaper.DeleteExtState("AudioPro", "template_path", false)
reaper.DeleteExtState("AudioPro", "original_name", false)
""")
    temp_script.close()

    # Ejecutar ReaScript
    cmd = [
        REAPER_EXE,
        '-nosplash',
        temp_script.name
    ]

    try:
        # Ejecutar Reaper en background
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Esperar un poco para que Reaper inicie y ejecute el script
        time.sleep(5)

        # Verificar si el proceso sigue corriendo
        if process.poll() is None:
            print_success("Audio agregado a sesión de Reaper - Reaper permanecerá abierto")
        else:
            # Si terminó, verificar el código de salida
            stdout, stderr = process.communicate()
            if process.returncode != 0:
                print_error(f"Error ejecutando ReaScript: {stderr}")
            else:
                print_success("Audio agregado a sesión de Reaper")
    except Exception as e:
        print_error(f"Error ejecutando ReaScript: {e}")
    finally:
        # Limpiar archivo temporal
        try:
            os.unlink(temp_script.name)
        except Exception:
            pass


def process_with_reaper_pipeline(
    file_bytes: bytes,
    original_name: str,
    source_dir: Optional[str] = None,
    use_elevenlabs: bool = True
) -> dict:
    """Pipeline completo con Reaper.

    Args:
        file_bytes: Bytes del archivo original
        original_name: Nombre del archivo original
        source_dir: Directorio de origen (opcional)
        use_elevenlabs: Si se debe usar ElevenLabs

    Returns:
        Dict con información del archivo procesado
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_name = f"{os.path.splitext(original_name)[0]}_{timestamp}"

    # 1) Guardar archivo original temporalmente
    tmp_input = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=os.path.splitext(original_name)[1]
    ).name
    with open(tmp_input, 'wb') as f:
        f.write(file_bytes)

    print_info(f"Procesando: {original_name}")

    # 2) Extraer audio
    print_info("Extrayendo audio...")
    audio_wav = extract_audio_wav16_mono(tmp_input)

    # 3) ElevenLabs Audio Isolation
    if use_elevenlabs and ELEVENLABS_API_KEY:
        print_info("Aplicando Audio Isolation (ElevenLabs)...")
        audio_wav_before = audio_wav
        audio_wav = process_audio_with_elevenlabs(audio_wav, ELEVENLABS_API_KEY, ELEVENLABS_BASE_URL)
        if audio_wav != audio_wav_before:
            print_success("ElevenLabs procesó correctamente")
        else:
            print_warning("ElevenLabs no procesó el audio - usando original")
    else:
        if not use_elevenlabs:
            print_warning("ElevenLabs deshabilitado - saltando Audio Isolation")
        else:
            print_warning("ElevenLabs no configurado - saltando Audio Isolation")

    # 4) Crear directorio de sesiones si no existe
    os.makedirs(REAPER_SESSIONS_DIR, exist_ok=True)

    # 5) Definir ruta de la nueva sesión
    session_path = os.path.join(REAPER_SESSIONS_DIR, f"{session_name}.rpp")

    print_info(f"Creando sesión de Reaper: {session_name}")
    print_info(f"Sesión se guardará en: {session_path}")

    # 6) Agregar audio a la sesión
    print_info("Agregando audio a sesión de Reaper...")

    # Obtener nombre original sin extensión para pasar a Reaper
    original_name_clean = os.path.splitext(original_name)[0]
    add_audio_to_reaper_session(session_path, audio_wav, original_name_clean)

    # 7) Esperar a que Reaper termine el render
    print_info("Esperando a que Reaper complete el render...")
    print_warning("Por favor, ten paciencia. El procesamiento con Reaper puede tomar varios minutos.")

    # Esperar hasta 10 minutos para que el archivo renderizado aparezca
    session_dir = os.path.dirname(session_path)
    expected_render = os.path.join(session_dir, f"{original_name_clean}_renderizado.wav")

    max_wait = 600  # 10 minutos
    elapsed = 0
    check_interval = 5  # Verificar cada 5 segundos

    while elapsed < max_wait:
        if os.path.exists(expected_render):
            # Esperar más tiempo para que Reaper termine de escribir y libere el archivo
            print_info("Archivo detectado - esperando que Reaper libere el archivo...")
            time.sleep(10)  # Esperar 10 segundos adicionales

            # Verificar que el archivo no esté bloqueado
            file_ready = False
            for attempt in range(5):
                try:
                    # Intentar abrir el archivo para verificar que no esté bloqueado
                    with open(expected_render, 'rb') as f:
                        f.read(1)
                    file_ready = True
                    break
                except (PermissionError, IOError):
                    print_warning(f"Archivo aún bloqueado, esperando... (intento {attempt + 1}/5)")
                    time.sleep(3)

            if file_ready:
                print_success(f"Render completado: {expected_render}")
                rendered_audio = expected_render
                break
            else:
                print_error("El archivo sigue bloqueado por Reaper")
                raise Exception("Archivo renderizado bloqueado")

        time.sleep(check_interval)
        elapsed += check_interval
        if elapsed % 30 == 0:  # Mostrar progreso cada 30 segundos
            print_info(f"Esperando render... ({elapsed}s / {max_wait}s)")
    else:
        print_error(f"Timeout esperando el archivo renderizado: {expected_render}")
        raise Exception("Timeout esperando render de Reaper")

    # Verificar que el render fue exitoso
    if not rendered_audio or not os.path.exists(rendered_audio):
        print_error("El render de Reaper no generó un archivo de salida")
        raise Exception("Render de Reaper falló")

    # 8) Determinar directorio de salida
    # SIEMPRE crear carpeta "procesados" en la ubicación del archivo original
    if source_dir:
        # Archivo local - guardar en [carpeta_original]/procesados/
        output_dir = os.path.join(source_dir, 'procesados')
        os.makedirs(output_dir, exist_ok=True)
        print_info(f"📂 Carpeta de salida: {output_dir}")
    else:
        # Archivo de Drive - crear carpeta procesados en la sesión de Reaper
        session_dir = os.path.dirname(session_path)
        output_dir = os.path.join(session_dir, 'procesados')
        os.makedirs(output_dir, exist_ok=True)
        print_info(f"📂 Carpeta de salida: {output_dir}")

    # 9) Procesar según tipo de archivo
    is_video = not is_audio_only_file(tmp_input)

    if is_video:
        # Mux audio con video
        print_info("🎬 Combinando audio procesado con video...")
        base_name = os.path.splitext(original_name)[0]
        final_out = os.path.join(output_dir, f"{base_name}_procesado.mp4")

        cmd = [
            'ffmpeg', '-y', '-i', tmp_input, '-i', rendered_audio,
            '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k',
            '-ar', '48000', '-map', '0:v:0', '-map', '1:a:0',
            '-shortest', final_out
        ]
        run_ffmpeg(cmd)
        print_success(f"✅ Video final: {final_out}")
    else:
        # Solo copiar audio procesado
        print_info("🎵 Copiando audio procesado...")
        base_name = os.path.splitext(original_name)[0]
        ext = os.path.splitext(original_name)[1]
        final_out = os.path.join(output_dir, f"{base_name}_procesado{ext}")
        shutil.copy(rendered_audio, final_out)
        print_success(f"✅ Audio final: {final_out}")

    # También copiar el render WAV de Reaper a la carpeta procesados
    if os.path.exists(rendered_audio):
        wav_name = f"{os.path.splitext(original_name)[0]}_render_reaper.wav"
        wav_output = os.path.join(output_dir, wav_name)
        try:
            shutil.copy(rendered_audio, wav_output)
            print_info(f"💾 Render de Reaper guardado: {wav_name}")
        except Exception as e:
            print_warning(f"No se pudo copiar el render WAV: {e}")

    # 10) Limpiar archivos temporales
    try:
        os.unlink(tmp_input)
        os.unlink(audio_wav)
    except Exception:
        pass

    print_success(f"Procesado completado: {os.path.basename(final_out)}")

    return {
        'original_name': original_name,
        'output_file': final_out,
        'reaper_session': session_path,
        'is_video': is_video,
        'is_local': source_dir is not None
    }


def process_from_path(file_path: str, use_elevenlabs: bool = True):
    """Procesa un archivo desde una ruta local.

    Args:
        file_path: Ruta al archivo
        use_elevenlabs: Si se debe usar ElevenLabs
    """
    print_info(f"\n📁 Procesando archivo local: {file_path}")

    result = get_bytes_from_local_path(file_path)
    if not result:
        return

    file_bytes, file_name, source_dir = result

    try:
        result = process_with_reaper_pipeline(file_bytes, file_name, source_dir, use_elevenlabs)
        print_success(f"\n{'=' * 60}")
        print_success("ARCHIVO PROCESADO EXITOSAMENTE")
        print_success(f"{'=' * 60}")
        print_info(f"📄 Original: {result['original_name']}")
        print_info(f"📂 Archivo procesado: {result['output_file']}")
        print_info(f"🎛️  Sesión de Reaper: {result['reaper_session']}")
        print_success(f"{'=' * 60}\n")
    except Exception as e:
        print_error(f"\n❌ Error procesando {file_name}: {e}\n")


def process_from_drive(drive_url: str, use_elevenlabs: bool = True):
    """Procesa un archivo desde Google Drive.

    Args:
        drive_url: URL de Google Drive
        use_elevenlabs: Si se debe usar ElevenLabs
    """
    print_info("\n🔗 Procesando archivo de Google Drive")

    result = get_bytes_from_drive(drive_url)
    if not result:
        return

    file_bytes, file_name = result

    try:
        result = process_with_reaper_pipeline(file_bytes, file_name, None, use_elevenlabs)
        print_success(f"\n{'=' * 60}")
        print_success("ARCHIVO PROCESADO EXITOSAMENTE")
        print_success(f"{'=' * 60}")
        print_info(f"📄 Original: {result['original_name']}")
        print_info(f"📂 Archivo procesado: {result['output_file']}")
        print_info(f"🎛️  Sesión de Reaper: {result['reaper_session']}")
        print_success(f"{'=' * 60}\n")
    except Exception as e:
        print_error(f"\n❌ Error procesando {file_name}: {e}\n")


def process_batch_from_file(file_list_path: str, use_elevenlabs: bool = True):
    """Procesa múltiples archivos desde un archivo de texto.

    Args:
        file_list_path: Ruta al archivo de texto con rutas/URLs
        use_elevenlabs: Si se debe usar ElevenLabs
    """
    if not os.path.exists(file_list_path):
        print_error(f"Archivo no encontrado: {file_list_path}")
        return

    with open(file_list_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    print_info(f"\n📋 Procesando {len(lines)} archivo(s) desde {file_list_path}\n")

    for idx, line in enumerate(lines, 1):
        print_info(f"\n{'=' * 60}")
        print_info(f"Procesando {idx}/{len(lines)}")
        print_info(f"{'=' * 60}")

        if line.startswith('http'):
            process_from_drive(line, use_elevenlabs)
        else:
            process_from_path(line, use_elevenlabs)


def interactive_menu():
    """Menú interactivo para procesar archivos."""
    print_banner()

    while True:
        print(f"\n{Fore.YELLOW}MENÚ PRINCIPAL{Style.RESET_ALL}")
        print(f"{Fore.CYAN}1.{Style.RESET_ALL} Procesar archivo desde ruta local")
        print(f"{Fore.CYAN}2.{Style.RESET_ALL} Procesar archivo desde Google Drive")
        print(f"{Fore.CYAN}3.{Style.RESET_ALL} Procesar lote desde archivo de texto")
        print(f"{Fore.CYAN}4.{Style.RESET_ALL} Configuración")
        print(f"{Fore.CYAN}5.{Style.RESET_ALL} Salir")

        choice = input(f"\n{Fore.GREEN}Selecciona una opción: {Style.RESET_ALL}").strip()

        if choice == '1':
            path = input(f"\n{Fore.CYAN}Ingresa la ruta del archivo: {Style.RESET_ALL}").strip()
            use_eleven = input(f"{Fore.CYAN}¿Usar ElevenLabs? (s/n) [s]: {Style.RESET_ALL}").strip().lower()
            use_eleven = use_eleven != 'n'
            process_from_path(path, use_eleven)

        elif choice == '2':
            url = input(f"\n{Fore.CYAN}Ingresa la URL de Google Drive: {Style.RESET_ALL}").strip()
            use_eleven = input(f"{Fore.CYAN}¿Usar ElevenLabs? (s/n) [s]: {Style.RESET_ALL}").strip().lower()
            use_eleven = use_eleven != 'n'
            process_from_drive(url, use_eleven)

        elif choice == '3':
            path = input(f"\n{Fore.CYAN}Ingresa la ruta del archivo de texto: {Style.RESET_ALL}").strip()
            use_eleven = input(f"{Fore.CYAN}¿Usar ElevenLabs? (s/n) [s]: {Style.RESET_ALL}").strip().lower()
            use_eleven = use_eleven != 'n'
            process_batch_from_file(path, use_eleven)

        elif choice == '4':
            print(f"\n{Fore.YELLOW}CONFIGURACIÓN ACTUAL:{Style.RESET_ALL}")
            print(f"Reaper EXE: {REAPER_EXE}")
            print(f"Template: {REAPER_TEMPLATE}")
            print(f"Sesiones: {REAPER_SESSIONS_DIR}")
            print(f"ElevenLabs API Key: {'✅ Configurada' if ELEVENLABS_API_KEY else '❌ No configurada'}")
            print(f"ElevenLabs URL: {ELEVENLABS_BASE_URL}")

        elif choice == '5':
            print(f"\n{Fore.GREEN}¡Hasta luego!{Style.RESET_ALL}\n")
            break

        else:
            print_error("Opción no válida")


def main():
    """Función principal."""
    parser = argparse.ArgumentParser(
        description='AudioPro CLI v1.7 - Procesamiento profesional con Reaper',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  # Modo interactivo
  python audiopro_cli.py

  # Procesar archivo local
  python audiopro_cli.py -f "C:\\Videos\\video.mp4"

  # Procesar desde Google Drive
  python audiopro_cli.py -d "https://drive.google.com/file/d/XXXXX"

  # Procesar lote de archivos
  python audiopro_cli.py -b "archivos.txt"

  # Sin ElevenLabs
  python audiopro_cli.py -f "video.mp4" --no-elevenlabs

Variables de entorno:
  ELEVENLABS_API_KEY    API key de ElevenLabs
  ELEVENLABS_BASE_URL   URL base de la API (default: https://api.elevenlabs.io)
        """
    )

    parser.add_argument('-f', '--file', help='Ruta del archivo a procesar')
    parser.add_argument('-d', '--drive', help='URL de Google Drive')
    parser.add_argument('-b', '--batch', help='Archivo de texto con lista de rutas/URLs')
    parser.add_argument('--no-elevenlabs', action='store_true', help='Desactivar ElevenLabs')

    args = parser.parse_args()

    # Si no hay argumentos, mostrar menú interactivo
    if not any([args.file, args.drive, args.batch]):
        interactive_menu()
    else:
        print_banner()
        use_elevenlabs = not args.no_elevenlabs

        if args.file:
            process_from_path(args.file, use_elevenlabs)
        elif args.drive:
            process_from_drive(args.drive, use_elevenlabs)
        elif args.batch:
            process_batch_from_file(args.batch, use_elevenlabs)


if __name__ == '__main__':
    main()
