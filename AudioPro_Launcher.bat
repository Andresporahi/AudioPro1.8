@echo off
REM ============================================================
REM   AudioPro v1.7 - Launcher
REM   Selector de interfaz
REM ============================================================

title AudioPro v1.7 - Launcher
color 0B

:MENU
cls
echo.
echo ============================================================
echo    AudioPro v1.7 - Reaper Edition
echo    Procesamiento Profesional de Audio/Video
echo ============================================================
echo.
echo    Selecciona el modo de inicio:
echo.
echo    [1] Interfaz Grafica (GUI) - Ventanas con botones
echo        Recomendado: Facil de usar, visual e intuitivo
echo.
echo    [2] Interfaz de Linea de Comandos (CLI) - Terminal
echo        Recomendado: Para automatizacion y scripts
echo.
echo    [3] Salir
echo.
echo ============================================================
echo.

set /p choice="Selecciona una opcion (1-3): "

if "%choice%"=="1" goto GUI
if "%choice%"=="2" goto CLI
if "%choice%"=="3" goto EXIT
goto INVALID

:GUI
echo.
echo Iniciando Interfaz Grafica...
echo.
call AudioPro_GUI.bat
goto END

:CLI
echo.
echo Iniciando Interfaz de Linea de Comandos...
echo.
call AudioPro_CLI.bat
goto END

:INVALID
echo.
echo Opcion invalida. Presiona cualquier tecla para volver...
pause >nul
goto MENU

:EXIT
echo.
echo Hasta luego!
echo.
exit /b 0

:END
echo.
echo Presiona cualquier tecla para volver al menu...
pause >nul
goto MENU

