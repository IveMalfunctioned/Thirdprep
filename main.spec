# -*- mode: python ; coding: utf-8 -*-

import sys, os
pythonDir = os.path.join(os.getenv('APPDATA'), 'Python', next((folder for folder in os.listdir(os.path.join(roaming, 'Python')) if folder.startswith('Python3')), None))
print(f"{pythonDir}\\site-packages\\Pmw")
if not os.path.exists(f"{pythonDir}\\site-packages\\Pmw"):
	print("Missing Pmw, install it with 'pip install Pmw'")
	exit()

block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('icon.ico', '.'), ('DiskCleanupFlags.reg', '.'), ('nircmdc.exe', '.'), (f"{pythonDir}\\site-packages\\Pmw", 'Pmw')],
    hiddenimports=['Pmw'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Thirdprep',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)
