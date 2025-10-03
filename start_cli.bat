@echo off
REM AudioPro CLI v1.7 - Script de inicio
REM Este archivo inicia la aplicación de línea de comandos

echo ========================================
echo   AudioPro CLI v1.7 - Reaper Edition
echo ========================================
echo.

REM Verificar que Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    pause
    exit /b 1
)

REM Verificar que FFmpeg está instalado
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo ADVERTENCIA: FFmpeg no está instalado o no está en el PATH
    echo La aplicación necesita FFmpeg para funcionar correctamente
    pause
)

REM Establecer variables de entorno de ElevenLabs (opcional)
REM Descomenta y configura tus credenciales aquí:
REM set ELEVENLABS_API_KEY=tu_api_key_aqui
REM set ELEVENLABS_BASE_URL=https://api.elevenlabs.io

echo Iniciando AudioPro CLI...
echo.

REM Ejecutar la aplicación CLI
python audiopro_cli.py %*

echo.
echo Presiona cualquier tecla para salir...
pause >nul


