"""
Funciones auxiliares para AudioPro CLI v1.7
Versión sin dependencias de Streamlit
"""

import os
import tempfile
import subprocess
import requests
import gdown
from typing import Optional, Tuple
from colorama import Fore, Style, init

# Inicializar colorama para colores en terminal
init(autoreset=True)


def print_info(message: str):
    """Imprime mensaje informativo."""
    print(f"{Fore.CYAN}ℹ️  {message}{Style.RESET_ALL}")


def print_success(message: str):
    """Imprime mensaje de éxito."""
    print(f"{Fore.GREEN}✅ {message}{Style.RESET_ALL}")


def print_warning(message: str):
    """Imprime mensaje de advertencia."""
    print(f"{Fore.YELLOW}⚠️  {message}{Style.RESET_ALL}")


def print_error(message: str):
    """Imprime mensaje de error."""
    print(f"{Fore.RED}❌ {message}{Style.RESET_ALL}")


def get_bytes_from_local_path(file_path: str) -> Optional[Tuple[bytes, str, str]]:
    """Obtiene bytes de un archivo desde una ruta local.

    Args:
        file_path: Ruta al archivo

    Returns:
        Tuple de (bytes, nombre_archivo, directorio_origen) o None
    """
    try:
        if not os.path.exists(file_path):
            print_error(f"Archivo no encontrado: {file_path}")
            return None

        with open(file_path, 'rb') as f:
            file_bytes = f.read()

        file_name = os.path.basename(file_path)
        source_dir = os.path.dirname(file_path)

        return file_bytes, file_name, source_dir

    except Exception as e:
        print_error(f"Error leyendo archivo {file_path}: {e}")
        return None


def get_bytes_from_drive(drive_url: str) -> Optional[Tuple[bytes, str]]:
    """Obtiene bytes de un archivo desde Google Drive.

    Args:
        drive_url: URL de Google Drive

    Returns:
        Tuple de (bytes, nombre_archivo) o None
    """
    try:
        # Extraer ID del archivo de la URL
        if 'id=' in drive_url:
            file_id = drive_url.split('id=')[1].split('&')[0]
        elif '/file/d/' in drive_url:
            file_id = drive_url.split('/file/d/')[1].split('/')[0]
        else:
            print_error("URL de Google Drive no válida")
            return None

        # Descargar archivo
        print_info("Descargando desde Google Drive...")
        download_url = f"https://drive.google.com/uc?id={file_id}"
        file_path = gdown.download(download_url, quiet=False)

        if not file_path:
            print_error("No se pudo descargar el archivo de Google Drive")
            return None

        # Leer bytes
        with open(file_path, 'rb') as f:
            file_bytes = f.read()

        file_name = os.path.basename(file_path)

        # Limpiar archivo temporal
        try:
            os.unlink(file_path)
        except Exception:
            pass

        return file_bytes, file_name

    except Exception as e:
        print_error(f"Error descargando de Google Drive: {e}")
        return None


def extract_audio_wav16_mono(input_file: str) -> str:
    """Extrae audio de un archivo y lo convierte a WAV mono 48kHz.

    Args:
        input_file: Ruta al archivo de entrada

    Returns:
        Ruta al archivo WAV generado
    """
    # Guardar audio extraído directamente en F:\00\00 Reaper\Eleven\
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    eleven_dir = r"F:\00\00 Reaper\Eleven"
    os.makedirs(eleven_dir, exist_ok=True)

    output_file = os.path.join(eleven_dir, f"extracted_{timestamp}.wav")

    cmd = [
        'ffmpeg', '-y', '-i', input_file,
        '-ac', '1',  # mono
        '-ar', '48000',  # 48kHz (estándar profesional)
        '-acodec', 'pcm_s16le',  # 16-bit PCM
        '-sample_fmt', 's16',  # Asegurar formato 16-bit
        output_file
    ]

    run_ffmpeg(cmd)
    print_info(f"Audio extraído guardado en: {output_file}")
    return output_file


def run_ffmpeg(cmd: list) -> None:
    """Ejecuta un comando FFmpeg.

    Args:
        cmd: Lista de argumentos del comando
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600
        )

        if result.returncode != 0:
            print_error(f"Error FFmpeg: {result.stderr}")
            raise Exception(f"FFmpeg failed: {result.stderr}")

    except subprocess.TimeoutExpired:
        print_error("FFmpeg excedió el tiempo límite (10 min)")
        raise Exception("FFmpeg timeout")
    except Exception as e:
        print_error(f"Error ejecutando FFmpeg: {e}")
        raise


def is_audio_only_file(file_path: str) -> bool:
    """Determina si un archivo es solo audio.

    Args:
        file_path: Ruta al archivo

    Returns:
        True si es solo audio, False si es video
    """
    audio_extensions = {'.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg'}
    _, ext = os.path.splitext(file_path.lower())
    return ext in audio_extensions


def process_audio_with_elevenlabs(audio_file: str, api_key: str, base_url: str = "https://api.elevenlabs.io") -> str:
    """Procesa audio con ElevenLabs Audio Isolation.

    Args:
        audio_file: Ruta al archivo de audio
        api_key: API key de ElevenLabs
        base_url: URL base de la API

    Returns:
        Ruta al archivo procesado
    """
    try:
        if not api_key:
            print_warning("API key de ElevenLabs no configurada")
            return audio_file

        # Preparar request con multipart/form-data
        headers = {
            'xi-api-key': api_key
        }

        # Endpoint de Audio Isolation
        url = f"{base_url}/audio-isolation"

        # Preparar archivos para multipart/form-data
        with open(audio_file, 'rb') as f:
            files = {
                'audio': (os.path.basename(audio_file), f, 'audio/wav')
            }

            # Enviar request con reintentos
            print_info(f"Enviando a ElevenLabs: {url}")
            print_info(f"Archivo: {os.path.basename(audio_file)}")
            max_retries = 5
            for attempt in range(max_retries):
                try:
                    print_info(f"Intento {attempt + 1}/{max_retries}...")
                    response = requests.post(url, headers=headers, files=files, timeout=180)
                    print_info(f"Respuesta recibida: {response.status_code}")
                    break
                except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                    if attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 3
                        print_warning(f"Intento {attempt + 1} falló, reintentando en {wait_time}s... ({e})")
                        import time
                        time.sleep(wait_time)
                    else:
                        print_error(f"Error de conexión con ElevenLabs después de {max_retries} intentos")
                        return audio_file

            if response.status_code == 200:
                # Guardar resultado temporal primero
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                eleven_dir = r"F:\00\00 Reaper\Eleven"
                os.makedirs(eleven_dir, exist_ok=True)

                # Guardar respuesta temporal
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav').name
                with open(temp_file, 'wb') as f:
                    f.write(response.content)

                # Convertir a WAV puro usando FFmpeg
                output_file = os.path.join(eleven_dir, f"elevenlabs_{timestamp}.wav")

                print_info("Convirtiendo a WAV puro compatible con Reaper...")
                cmd = [
                    'ffmpeg', '-y', '-i', temp_file,
                    '-ar', '48000',  # 48kHz
                    '-ac', '1',  # Mono
                    '-acodec', 'pcm_s16le',  # 16-bit PCM
                    '-sample_fmt', 's16',  # Asegurar formato 16-bit
                    '-fflags', '+bitexact',  # Sin metadata
                    '-flags:v', '+bitexact',
                    '-flags:a', '+bitexact',
                    output_file
                ]

                run_ffmpeg(cmd)

                # Eliminar archivo temporal
                try:
                    os.unlink(temp_file)
                except Exception:
                    pass

                print_success(f"Voice Isolator aplicado y convertido a WAV puro: {output_file}")
                return output_file
            elif response.status_code == 401:
                print_error("Error de autenticación ElevenLabs - Verifica tu API key")
                return audio_file
            elif response.status_code == 404:
                print_warning("Voice Isolator no disponible en tu cuenta de ElevenLabs")
                return audio_file
            elif response.status_code == 429:
                print_error("Límite de rate excedido en ElevenLabs - Espera unos minutos")
                return audio_file
            else:
                print_error(f"Error ElevenLabs: {response.status_code} - {response.text}")
                return audio_file

    except Exception as e:
        print_error(f"Error procesando con ElevenLabs: {e}")
        return audio_file
