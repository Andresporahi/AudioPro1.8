@echo off
REM ============================================================
REM  AudioPro CLI v1.7 - Instalador de Acceso Directo
REM ============================================================

echo.
echo ============================================================
echo   AudioPro CLI v1.7 - Instalador de Acceso Directo
echo ============================================================
echo.

REM Crear script VBScript temporal
set "VBS_SCRIPT=%TEMP%\crear_acceso_audiopro.vbs"

echo Set oWS = WScript.CreateObject("WScript.Shell") > "%VBS_SCRIPT%"
echo sLinkFile = oWS.SpecialFolders("Desktop") ^& "\AudioPro CLI.lnk" >> "%VBS_SCRIPT%"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%VBS_SCRIPT%"
echo oLink.TargetPath = "%~dp0AudioPro_CLI.bat" >> "%VBS_SCRIPT%"
echo oLink.WorkingDirectory = "%~dp0" >> "%VBS_SCRIPT%"
echo oLink.Description = "AudioPro CLI v1.7 - Procesamiento Profesional" >> "%VBS_SCRIPT%"
echo oLink.IconLocation = "shell32.dll,137" >> "%VBS_SCRIPT%"
echo oLink.Save >> "%VBS_SCRIPT%"

REM Ejecutar el script VBScript
cscript //nologo "%VBS_SCRIPT%"

REM Limpiar script temporal
del "%VBS_SCRIPT%"

REM Verificar si se creó el acceso directo
if exist "%USERPROFILE%\Desktop\AudioPro CLI.lnk" (
    echo.
    echo [EXITO] Acceso directo creado exitosamente!
    echo.
    echo El acceso directo "AudioPro CLI" esta ahora en tu escritorio
    echo.
    echo Ahora puedes:
    echo   1. Hacer doble clic en el acceso directo desde tu escritorio
    echo   2. O ejecutar directamente AudioPro_CLI.bat
    echo.
) else (
    echo.
    echo [ERROR] No se pudo crear el acceso directo
    echo Intenta crearlo manualmente o ejecuta como administrador
    echo.
)

echo ============================================================
echo.
echo Presiona cualquier tecla para salir...
pause >nul

