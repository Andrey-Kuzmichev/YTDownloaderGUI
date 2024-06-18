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
                        StringStruct('CompanyName', 'Andrey-Kuzmichev'),
                        StringStruct('FileDescription', 'YouTube Downloader GUI'),
                        StringStruct('FileVersion', '{major}.{minor}.{build}_{revision}MSK'),
                        StringStruct('InternalName', 'YouTube Downloader GUI'),
                        StringStruct('LegalCopyright', '© Andrey-Kuzmichev {major}'),
                        StringStruct('OriginalFilename', 'YTDownloaderGUI.exe'),
                        StringStruct('ProductName', 'YTDownloaderGUI'),
                        StringStruct('ProductVersion', '{major}.{minor}.{build}_{revision}MSK'),
                        StringStruct('TimeZone', 'MSK')
                    ]
                ),
                StringTable(
                    '041904E4',
                    [
                        StringStruct('CompanyName', 'Andrey-Kuzmichev'),
                        StringStruct('FileDescription', 'YouTube Downloader GUI'),
                        StringStruct('FileVersion', '{major}.{minor}.{build}_{revision}MSK'),
                        StringStruct('InternalName', 'YouTube Downloader GUI'),
                        StringStruct('LegalCopyright', '© Andrey-Kuzmichev {major}'),
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
