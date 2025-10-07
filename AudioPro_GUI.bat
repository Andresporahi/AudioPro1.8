@echo off
REM ============================================================
REM   AudioPro GUI v1.7 - Interfaz Gráfica
REM ============================================================

REM Cambiar al directorio del proyecto
cd /d "D:\CURSOR\Audiopro 1.7"

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado o no esta en el PATH
    echo.
    echo Instala Python desde: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Verificar que exista el script principal
if not exist "audiopro_gui.py" (
    echo [ERROR] No se encuentra audiopro_gui.py
    echo Verifica que estas en el directorio correcto
    echo.
    pause
    exit /b 1
)

REM Configuración de ElevenLabs (opcional)
REM Descomenta y configura tus credenciales aquí:
REM set ELEVENLABS_API_KEY=tu_api_key_aqui
REM set ELEVENLABS_BASE_URL=https://api.elevenlabs.io

REM Iniciar la aplicación GUI
pythonw audiopro_gui.py

REM Si pythonw no funciona, usar python normal
if errorlevel 1 (
    python audiopro_gui.py
)

