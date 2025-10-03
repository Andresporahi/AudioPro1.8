@echo off
REM ============================================================
REM  AudioPro v1.7 - Instalador de Accesos Directos
REM  Crea accesos directos en el escritorio para GUI y CLI
REM ============================================================

echo.
echo ============================================================
echo   AudioPro v1.7 - Instalador de Accesos Directos
echo ============================================================
echo.

REM Verificar que existen los archivos necesarios
if not exist "AudioPro_GUI.bat" (
    echo [ERROR] No se encuentra AudioPro_GUI.bat
    pause
    exit /b 1
)

if not exist "AudioPro_CLI.bat" (
    echo [ERROR] No se encuentra AudioPro_CLI.bat
    pause
    exit /b 1
)

if not exist "AudioPro_Launcher.bat" (
    echo [ERROR] No se encuentra AudioPro_Launcher.bat
    pause
    exit /b 1
)

echo Creando accesos directos en el escritorio...
echo.

REM ============================================================
REM Acceso directo principal (Launcher)
REM ============================================================

set "VBS_SCRIPT=%TEMP%\crear_acceso_launcher.vbs"

echo Set oWS = WScript.CreateObject("WScript.Shell") > "%VBS_SCRIPT%"
echo sLinkFile = oWS.SpecialFolders("Desktop") ^& "\AudioPro v1.7.lnk" >> "%VBS_SCRIPT%"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%VBS_SCRIPT%"
echo oLink.TargetPath = "%~dp0AudioPro_Launcher.bat" >> "%VBS_SCRIPT%"
echo oLink.WorkingDirectory = "%~dp0" >> "%VBS_SCRIPT%"
echo oLink.Description = "AudioPro v1.7 - Selector de Interfaz" >> "%VBS_SCRIPT%"
echo oLink.IconLocation = "shell32.dll,137" >> "%VBS_SCRIPT%"
echo oLink.Save >> "%VBS_SCRIPT%"

cscript //nologo "%VBS_SCRIPT%"
del "%VBS_SCRIPT%"

if exist "%USERPROFILE%\Desktop\AudioPro v1.7.lnk" (
    echo [OK] Acceso directo principal creado
) else (
    echo [ERROR] No se pudo crear el acceso directo principal
)

echo.

REM ============================================================
REM Acceso directo GUI
REM ============================================================

set "VBS_SCRIPT=%TEMP%\crear_acceso_gui.vbs"

echo Set oWS = WScript.CreateObject("WScript.Shell") > "%VBS_SCRIPT%"
echo sLinkFile = oWS.SpecialFolders("Desktop") ^& "\AudioPro GUI.lnk" >> "%VBS_SCRIPT%"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%VBS_SCRIPT%"
echo oLink.TargetPath = "%~dp0AudioPro_GUI.bat" >> "%VBS_SCRIPT%"
echo oLink.WorkingDirectory = "%~dp0" >> "%VBS_SCRIPT%"
echo oLink.Description = "AudioPro v1.7 - Interfaz Grafica" >> "%VBS_SCRIPT%"
echo oLink.IconLocation = "shell32.dll,165" >> "%VBS_SCRIPT%"
echo oLink.Save >> "%VBS_SCRIPT%"

cscript //nologo "%VBS_SCRIPT%"
del "%VBS_SCRIPT%"

if exist "%USERPROFILE%\Desktop\AudioPro GUI.lnk" (
    echo [OK] Acceso directo GUI creado
) else (
    echo [ERROR] No se pudo crear el acceso directo GUI
)

echo.

REM ============================================================
REM Acceso directo CLI
REM ============================================================

set "VBS_SCRIPT=%TEMP%\crear_acceso_cli.vbs"

echo Set oWS = WScript.CreateObject("WScript.Shell") > "%VBS_SCRIPT%"
echo sLinkFile = oWS.SpecialFolders("Desktop") ^& "\AudioPro CLI.lnk" >> "%VBS_SCRIPT%"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%VBS_SCRIPT%"
echo oLink.TargetPath = "%~dp0AudioPro_CLI.bat" >> "%VBS_SCRIPT%"
echo oLink.WorkingDirectory = "%~dp0" >> "%VBS_SCRIPT%"
echo oLink.Description = "AudioPro v1.7 - Terminal CLI" >> "%VBS_SCRIPT%"
echo oLink.IconLocation = "shell32.dll,137" >> "%VBS_SCRIPT%"
echo oLink.Save >> "%VBS_SCRIPT%"

cscript //nologo "%VBS_SCRIPT%"
del "%VBS_SCRIPT%"

if exist "%USERPROFILE%\Desktop\AudioPro CLI.lnk" (
    echo [OK] Acceso directo CLI creado
) else (
    echo [ERROR] No se pudo crear el acceso directo CLI
)

echo.
echo ============================================================
echo.
echo [COMPLETADO] Se crearon 3 accesos directos en tu escritorio:
echo.
echo   1. "AudioPro v1.7" - Selector (te permite elegir GUI o CLI)
echo   2. "AudioPro GUI" - Interfaz grafica directa
echo   3. "AudioPro CLI" - Terminal de comandos directa
echo.
echo ============================================================
echo.
echo Presiona cualquier tecla para salir...
pause >nul

