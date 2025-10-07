"""
Gestor de configuración para AudioPro 1.8
Maneja la configuración desde archivo config.ini
"""

import os
import configparser
from pathlib import Path


class ConfigManager:
    """Gestor de configuración de AudioPro."""
    
    def __init__(self, config_file='config.ini'):
        """Inicializar gestor de configuración.
        
        Args:
            config_file: Ruta al archivo de configuración
        """
        # Determinar ruta del archivo de configuración
        if getattr(sys, 'frozen', False):
            # Ejecutable empaquetado con PyInstaller
            self.app_dir = os.path.dirname(sys.executable)
        else:
            # Script Python normal
            self.app_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.config_path = os.path.join(self.app_dir, config_file)
        self.config = configparser.ConfigParser()
        
        # Cargar o crear configuración
        self.load_or_create_config()
    
    def load_or_create_config(self):
        """Cargar configuración existente o crear con valores por defecto."""
        if os.path.exists(self.config_path):
            self.config.read(self.config_path)
        else:
            self.create_default_config()
    
    def create_default_config(self):
        """Crear archivo de configuración con valores por defecto."""
        self.config['Paths'] = {
            'REAPER_EXE': r'C:\Program Files\REAPER (x64)\reaper.exe',
            'REAPER_TEMPLATE': r'F:\00\00 Reaper\00 Voces.rpp',
            'REAPER_SESSIONS_DIR': r'F:\00\00 Reaper\Procesados',
            'REAPER_ELEVEN_DIR': r'F:\00\00 Reaper\Eleven',
        }
        
        self.config['ElevenLabs'] = {
            'API_KEY': '',
            'BASE_URL': 'https://api.elevenlabs.io',
        }
        
        self.config['Settings'] = {
            'DEFAULT_BIT_DEPTH': '24',
            'DEFAULT_SAMPLE_RATE': '48000',
            'LUFS_TARGET': '-16',
        }
        
        self.save_config()
    
    def save_config(self):
        """Guardar configuración actual al archivo."""
        with open(self.config_path, 'w') as f:
            self.config.write(f)
    
    def get(self, section, key, fallback=None):
        """Obtener valor de configuración.
        
        Args:
            section: Sección del archivo .ini
            key: Clave a buscar
            fallback: Valor por defecto si no existe
        
        Returns:
            Valor de configuración
        """
        return self.config.get(section, key, fallback=fallback)
    
    def set(self, section, key, value):
        """Establecer valor de configuración.
        
        Args:
            section: Sección del archivo .ini
            key: Clave a establecer
            value: Valor a guardar
        """
        if section not in self.config:
            self.config[section] = {}
        
        self.config[section][key] = str(value)
        self.save_config()
    
    def get_reaper_exe(self):
        """Obtener ruta del ejecutable de Reaper."""
        return self.get('Paths', 'REAPER_EXE', 
                       r'C:\Program Files\REAPER (x64)\reaper.exe')
    
    def get_reaper_template(self):
        """Obtener ruta del template de Reaper."""
        return self.get('Paths', 'REAPER_TEMPLATE',
                       r'F:\00\00 Reaper\00 Voces.rpp')
    
    def get_reaper_sessions_dir(self):
        """Obtener directorio de sesiones de Reaper."""
        return self.get('Paths', 'REAPER_SESSIONS_DIR',
                       r'F:\00\00 Reaper\Procesados')
    
    def get_reaper_eleven_dir(self):
        """Obtener directorio Eleven de Reaper."""
        eleven_dir = self.get('Paths', 'REAPER_ELEVEN_DIR',
                             r'F:\00\00 Reaper\Eleven')
        # Crear si no existe
        os.makedirs(eleven_dir, exist_ok=True)
        return eleven_dir
    
    def get_elevenlabs_api_key(self):
        """Obtener API key de ElevenLabs."""
        # Intentar primero desde variable de entorno
        api_key = os.getenv('ELEVENLABS_API_KEY')
        if api_key:
            return api_key
        # Luego desde config
        return self.get('ElevenLabs', 'API_KEY', '')
    
    def get_elevenlabs_base_url(self):
        """Obtener URL base de ElevenLabs."""
        base_url = os.getenv('ELEVENLABS_BASE_URL')
        if base_url:
            return base_url
        return self.get('ElevenLabs', 'BASE_URL', 
                       'https://api.elevenlabs.io')


# Instancia global de configuración
import sys
_config = None


def get_config():
    """Obtener instancia global de configuración."""
    global _config
    if _config is None:
        _config = ConfigManager()
    return _config

