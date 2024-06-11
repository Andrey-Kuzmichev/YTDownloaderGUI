import datetime


def generate_version_file():
    msk = datetime.timezone(datetime.timedelta(hours=3))
    now = datetime.datetime.now(msk)

    major = now.year
    minor = now.month
    build = now.day
    revision = now.hour * 100 + now.minute

    version_template = f"""VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=({major}, {minor}, {build}, {revision}),
        prodvers=({major}, {minor}, {build}, {revision}),
        mask=0x3f,
        flags=0x0,
        OS=0x4,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0)
    ),
    kids=[
        StringFileInfo(
            [
                StringTable(
                    '040904B0',
                    [
                        StringStruct('CompanyName', 'Andrey Kuzmichev'),
                        StringStruct('FileDescription', 'Versatile YouTube downloader with a user-friendly GUI. Supports audio and video stream selection.'),
                        StringStruct('FileVersion', '{major}.{minor}.{build}_{revision}MSK'),
                        StringStruct('InternalName', 'YTDownloaderGUI'),
                        StringStruct('LegalCopyright', '© Andrey Kuzmichev {major}'),
                        StringStruct('OriginalFilename', 'YTDownloaderGUI.exe'),
                        StringStruct('ProductName', 'YTDownloaderGUI'),
                        StringStruct('ProductVersion', '{major}.{minor}.{build}_{revision}MSK'),
                        StringStruct('TimeZone', 'MSK')
                    ]
                ),
                StringTable(
                    '041904E4',
                    [
                        StringStruct('CompanyName', 'Андрей Кузьмичев'),
                        StringStruct('FileDescription', 'Универсальный загрузчик YouTube с удобным графическим интерфейсом. Поддерживает выбор аудио и видео потоков.'),
                        StringStruct('FileVersion', '{major}.{minor}.{build}_{revision}MSK'),
                        StringStruct('InternalName', 'YTDownloaderGUI'),
                        StringStruct('LegalCopyright', '© Андрей Кузьмичев {major}'),
                        StringStruct('OriginalFilename', 'YTDownloaderGUI.exe'),
                        StringStruct('ProductName', 'YTDownloaderGUI'),
                        StringStruct('ProductVersion', '{major}.{minor}.{build}_{revision}MSK'),
                        StringStruct('TimeZone', 'MSK')
                    ]
                )
            ]
        ),
        VarFileInfo(
            [
                VarStruct('Translation', [1033, 1200]),
                VarStruct('Translation', [1049, 1251])
            ]
        )
    ]
)"""
    with open('version.txt', 'w', encoding='utf-8') as file:
        file.write(version_template)
