@echo off
echo ========================================
echo   AudioPro v1.7 - Reaper Edition
echo ========================================
echo.

REM Verificar Python
python --version > nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado
    echo Por favor instala Python 3.9 o superior
    pause
    exit /b 1
)

REM Verificar FFmpeg
ffmpeg -version > nul 2>&1
if errorlevel 1 (
    echo ERROR: FFmpeg no esta instalado
    echo Por favor ejecuta setup_ffmpeg.py primero
    pause
    exit /b 1
)

REM Verificar Reaper
if not exist "C:\Program Files\REAPER (x64)\reaper.exe" (
    echo ADVERTENCIA: Reaper no encontrado en C:\Program Files\REAPER ^(x64^)\
    echo Asegurate de ajustar la ruta en app.py si Reaper esta en otra ubicacion
    echo.
)

REM Verificar template
if not exist "F:\00\00 Reaper\00 Voces.rpp" (
    echo ADVERTENCIA: Template de Reaper no encontrado
    echo Buscando en: F:\00\00 Reaper\00 Voces.rpp
    echo Asegurate de ajustar la ruta en app.py
    echo.
)

REM Crear directorio de sesiones si no existe
if not exist "F:\CURSOS\2025\Q3" (
    echo Creando directorio de sesiones...
    mkdir "F:\CURSOS\2025\Q3" 2>nul
)

echo.
echo Iniciando AudioPro v1.7...
echo.
echo IMPORTANTE:
echo - Esta version usa Reaper para procesamiento profesional
echo - El render puede tomar 3-5 minutos por archivo
echo - Asegurate de tener suficiente espacio en disco
echo - Las sesiones se guardan en F:\CURSOS\2025\Q3
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

streamlit run app.py

pause
