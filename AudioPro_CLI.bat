@echo off
REM ============================================================
REM   AudioPro CLI v1.7 - Acceso Directo
REM ============================================================

REM Cambiar al directorio del proyecto
cd /d "D:\CURSOR\Audiopro 1.7"

REM Establecer título de la ventana
title AudioPro CLI v1.7 - Reaper Edition

REM Colores (opcional - solo funciona en Windows 10+)
color 0B

REM Banner
echo.
echo ============================================================
echo    AudioPro CLI v1.7 - Reaper Edition
echo    Procesamiento Profesional de Audio/Video
echo ============================================================
echo.

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

REM Verificar FFmpeg
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo [ADVERTENCIA] FFmpeg no esta instalado
    echo La aplicacion necesita FFmpeg para funcionar
    echo.
    echo Instala FFmpeg desde: https://ffmpeg.org/download.html
    echo.
    pause
)

REM Verificar que exista el script principal
if not exist "audiopro_cli.py" (
    echo [ERROR] No se encuentra audiopro_cli.py
    echo Verifica que estas en el directorio correcto
    echo.
    pause
    exit /b 1
)

REM Configuración de ElevenLabs (opcional)
REM Descomenta y configura tus credenciales aquí:
REM set ELEVENLABS_API_KEY=tu_api_key_aqui
REM set ELEVENLABS_BASE_URL=https://api.elevenlabs.io

REM Iniciar la aplicación
cls
python audiopro_cli.py

REM Mantener ventana abierta si hay error
if errorlevel 1 (
    echo.
    echo ============================================================
    echo   Hubo un error. Presiona cualquier tecla para salir...
    echo ============================================================
    pause >nul
)

