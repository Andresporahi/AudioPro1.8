# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file para AudioPro 1.8 GUI

block_cipher = None

# Archivos de datos a incluir
datas = [
    ('add_multiple_media.lua', '.'),
    ('add_audio_to_session.lua', '.'),
    ('render_session.lua', '.'),
    ('test_reaper.lua', '.'),
    ('*.md', '.'),
    ('*.txt', '.'),
    ('requirements.txt', '.'),
    ('cspell.json', '.'),
]

# Módulos hidden imports (dependencias no detectadas automáticamente)
hiddenimports = [
    'audio_utils_cli',
    'config_manager',
    'configparser',
    'queue',
    'threading',
    'tkinter',
    'tkinter.ttk',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'tkinter.scrolledtext',
]

a = Analysis(
    ['audiopro_gui.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'PIL',
        'jupyter',
        'notebook',
        'streamlit',  # No necesitamos streamlit en la versión GUI
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AudioPro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No mostrar consola (GUI pura)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Puedes agregar un ícono .ico aquí
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AudioPro',
)

