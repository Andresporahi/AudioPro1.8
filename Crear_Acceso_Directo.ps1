# ============================================================
# AudioPro CLI v1.7 - Instalador de Acceso Directo
# Este script crea un acceso directo en el escritorio
# ============================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  AudioPro CLI v1.7 - Instalador de Acceso Directo" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Obtener ruta del escritorio
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "AudioPro CLI.lnk"

# Ruta del script bat
$ScriptPath = Join-Path $PSScriptRoot "AudioPro_CLI.bat"

# Verificar que existe el script
if (-not (Test-Path $ScriptPath)) {
    Write-Host "[ERROR] No se encuentra AudioPro_CLI.bat" -ForegroundColor Red
    Write-Host "Verifica que el archivo existe en: $ScriptPath" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

# Crear el acceso directo
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $ScriptPath
$Shortcut.WorkingDirectory = $PSScriptRoot
$Shortcut.Description = "AudioPro CLI v1.7 - Procesamiento Profesional de Audio/Video"
$Shortcut.IconLocation = "shell32.dll,137"  # Icono de nota musical
$Shortcut.Save()

# Verificar que se creó
if (Test-Path $ShortcutPath) {
    Write-Host "[EXITO] Acceso directo creado exitosamente!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Ubicacion: $ShortcutPath" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Ahora puedes:" -ForegroundColor Yellow
    Write-Host "  1. Hacer doble clic en 'AudioPro CLI' desde tu escritorio" -ForegroundColor White
    Write-Host "  2. O ejecutar directamente AudioPro_CLI.bat" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "[ERROR] No se pudo crear el acceso directo" -ForegroundColor Red
    Write-Host ""
}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Presiona cualquier tecla para salir..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

