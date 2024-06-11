import os

import PyInstaller.__main__

from auxiliary.generate_version_file import generate_version_file

if os.path.isfile('YTDownloaderGUI.spec'):
    generate_version_file()

    PyInstaller.__main__.run([
        'YTDownloaderGUI.spec',
        '--clean',
        '--noconfirm'
    ])
else:
    PyInstaller.__main__.run([
        '../__main__.py',
        '--clean',
        '--onefile',
        '--windowed',
        '--noconsole',
        '--name', 'YTDownloaderGUI',
        '--icon', '../images/app_icon.ico',
        '--add-data', '../images/russia.png:images',
        '--add-data', '../images/app_icon.ico:images'
    ])
