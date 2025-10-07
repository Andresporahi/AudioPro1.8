@echo off
REM Script para construir el instalador de AudioPro 1.8
REM Ejecutar como administrador

echo ===================================
echo AudioPro 1.8 - Build Installer
echo ===================================
echo.

REM Verificar que estamos en el directorio correcto
if not exist "audiopro_gui.py" (
    echo ERROR: No se encuentra audiopro_gui.py
    echo Por favor ejecuta este script desde la carpeta del proyecto
    pause
    exit /b 1
)

REM Paso 1: Instalar PyInstaller si no está instalado
echo [1/4] Verificando PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Instalando PyInstaller...
    pip install pyinstaller
) else (
    echo PyInstaller ya esta instalado
)

REM Paso 2: Crear ejecutable con PyInstaller
echo.
echo [2/4] Creando ejecutable con PyInstaller...
echo Esto puede tardar varios minutos...
pyinstaller --clean audiopro_gui.spec

if errorlevel 1 (
    echo ERROR: Fallo la creacion del ejecutable
    pause
    exit /b 1
)

REM Paso 3: Verificar que Inno Setup esté instalado
echo.
echo [3/4] Verificando Inno Setup...
set INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe
if not exist "%INNO_PATH%" (
    echo.
    echo ADVERTENCIA: Inno Setup no encontrado
    echo Por favor instala Inno Setup desde: https://jrsoftware.org/isdl.php
    echo.
    echo Presiona cualquier tecla para abrir el sitio de descarga...
    pause >nul
    start https://jrsoftware.org/isdl.php
    echo.
    echo Despues de instalar Inno Setup, ejecuta este script nuevamente
    pause
    exit /b 1
)

REM Paso 4: Crear instalador con Inno Setup
echo.
echo [4/4] Creando instalador con Inno Setup...
"%INNO_PATH%" audiopro_installer.iss

if errorlevel 1 (
    echo ERROR: Fallo la creacion del instalador
    pause
    exit /b 1
)

echo.
echo ===================================
echo INSTALADOR CREADO EXITOSAMENTE!
echo ===================================
echo.
echo El instalador se encuentra en:
echo Output\AudioPro_1.8_Setup.exe
echo.
echo Tamano aproximado: ~100-150 MB
echo.
pause

