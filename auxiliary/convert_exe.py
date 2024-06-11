import PyInstaller.__main__

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
