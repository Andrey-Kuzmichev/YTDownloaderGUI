# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['..\\__main__.py'],
    pathex=['..\\__main__.py'],
    binaries=[],
    datas=[
        ('../images/russia.png', 'images'),
        ('../images/app_icon.ico', 'images')
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='YTDownloaderGUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    version='version.txt',
    icon='..\\images\\app_icon.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='YTDownloaderGUI'
)

app = BUNDLE(
    coll,
    name='YTDownloaderGUI',
    icon='..\\images\\app_icon.ico',
    version='version.txt',
    bundle_identifier=None
)
