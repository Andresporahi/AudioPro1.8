@echo off
REM ============================================================
REM  AudioPro CLI v1.7 - Ejemplos de Uso
REM ============================================================

echo.
echo ============================================================
echo   EJEMPLOS DE USO - AudioPro CLI v1.7
echo ============================================================
echo.

echo EJEMPLO 1: Modo Interactivo
echo ---------------------------
echo Comando: python audiopro_cli.py
echo.
echo Esto abre un menu donde puedes seleccionar opciones
echo.

echo EJEMPLO 2: Procesar un archivo local
echo -------------------------------------
echo Comando: python audiopro_cli.py -f "C:\Videos\mi_video.mp4"
echo.
echo Reemplaza "C:\Videos\mi_video.mp4" con la ruta de tu archivo
echo.

echo EJEMPLO 3: Procesar desde Google Drive
echo ---------------------------------------
echo Comando: python audiopro_cli.py -d "https://drive.google.com/file/d/XXXXX"
echo.
echo Reemplaza XXXXX con el ID de tu archivo de Drive
echo.

echo EJEMPLO 4: Procesar lote de archivos
echo -------------------------------------
echo Comando: python audiopro_cli.py -b "mis_archivos.txt"
echo.
echo Donde mis_archivos.txt contiene una lista de rutas/URLs
echo.

echo EJEMPLO 5: Sin ElevenLabs
echo --------------------------
echo Comando: python audiopro_cli.py -f "video.mp4" --no-elevenlabs
echo.
echo Usa --no-elevenlabs para saltar el procesamiento de ElevenLabs
echo.

echo ============================================================
echo   PRUEBA LA APLICACION
echo ============================================================
echo.
echo Presiona una tecla para iniciar la app en modo interactivo...
pause >nul

echo.
echo Iniciando AudioPro CLI en modo interactivo...
echo.
python audiopro_cli.py

