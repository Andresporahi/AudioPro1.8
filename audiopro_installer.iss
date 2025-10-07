; Script de Inno Setup para AudioPro 1.8
; Instalador profesional para Windows

#define MyAppName "AudioPro"
#define MyAppVersion "1.8"
#define MyAppPublisher "Andresporahi"
#define MyAppURL "https://github.com/Andresporahi/AudioPro1.8"
#define MyAppExeName "AudioPro.exe"

[Setup]
; Información de la aplicación
AppId={{B8F4A9C0-1D3E-4B5F-9A7C-2E8D6F1B4A3C}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=
OutputDir=Output
OutputBaseFilename=AudioPro_{#MyAppVersion}_Setup
SetupIconFile=
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; Archivos principales de la aplicación
Source: "dist\AudioPro\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "add_multiple_media.lua"; DestDir: "{app}"; Flags: ignoreversion
Source: "add_audio_to_session.lua"; DestDir: "{app}"; Flags: ignoreversion
Source: "render_session.lua"; DestDir: "{app}"; Flags: ignoreversion
Source: "test_reaper.lua"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "VERSION_1.8.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "CALIDAD_SIN_PERDIDA.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "VIDEO_TIMELINE_RENDER.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "PROCESAMIENTO_BATCH.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "INSTALACION_COMPLETA.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "requirements.txt"; DestDir: "{app}"; Flags: ignoreversion

; Crear directorios necesarios
[Dirs]
Name: "{app}\temp"
Name: "{app}\logs"

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Documentación"; Filename: "{app}\README.md"
Name: "{group}\Guía de Video"; Filename: "{app}\VIDEO_TIMELINE_RENDER.md"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
var
  ReaperPathPage: TInputDirWizardPage;
  FFmpegDownloadPage: TWizardPage;
  FFmpegPathEdit: TEdit;
  ReaperSessionsPathEdit: TEdit;
  ReaperTemplatePathEdit: TEdit;

procedure InitializeWizard;
begin
  { Página para configurar rutas de Reaper }
  ReaperPathPage := CreateInputDirPage(wpSelectDir,
    'Configuración de Reaper', 'Por favor especifica las rutas de Reaper',
    'AudioPro necesita saber dónde está instalado Reaper y dónde guardar las sesiones.',
    False, '');
  
  ReaperPathPage.Add('Ruta de Reaper.exe:');
  ReaperPathPage.Values[0] := 'C:\Program Files\REAPER (x64)\reaper.exe';
  
  ReaperPathPage.Add('Directorio de sesiones procesadas:');
  ReaperPathPage.Values[1] := 'F:\00\00 Reaper\Procesados';
  
  ReaperPathPage.Add('Template de Reaper (archivo .rpp):');
  ReaperPathPage.Values[2] := 'F:\00\00 Reaper\00 Voces.rpp';
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ConfigFile: string;
  ConfigContent: TArrayOfString;
begin
  if CurStep = ssPostInstall then
  begin
    { Crear archivo de configuración }
    ConfigFile := ExpandConstant('{app}\config.ini');
    
    SetArrayLength(ConfigContent, 3);
    ConfigContent[0] := '[Paths]';
    ConfigContent[1] := 'REAPER_EXE=' + ReaperPathPage.Values[0];
    ConfigContent[2] := 'REAPER_SESSIONS_DIR=' + ReaperPathPage.Values[1];
    ConfigContent[3] := 'REAPER_TEMPLATE=' + ReaperPathPage.Values[2];
    
    SaveStringsToFile(ConfigFile, ConfigContent, False);
    
    { Crear directorio Eleven si no existe }
    if not DirExists('F:\00\00 Reaper\Eleven') then
      CreateDir('F:\00\00 Reaper\Eleven');
      
    { Crear directorio Procesados si no existe }
    if not DirExists(ReaperPathPage.Values[1]) then
      CreateDir(ReaperPathPage.Values[1]);
  end;
end;

[Messages]
spanish.WelcomeLabel2=Esto instalará [name/ver] en tu computadora.%n%nNOTA: Reaper debe instalarse por separado. Puedes descargarlo desde https://www.reaper.fm%n%nSe recomienda cerrar todas las demás aplicaciones antes de continuar.
english.WelcomeLabel2=This will install [name/ver] on your computer.%n%nNOTE: Reaper must be installed separately. You can download it from https://www.reaper.fm%n%nIt is recommended that you close all other applications before continuing.

