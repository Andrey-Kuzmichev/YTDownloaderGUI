from tkinter import Tk

from pytubefix.innertube import _default_clients

from src.gui import App
from src.utils import resource_path

# Andrey Kuzmichev
# Telegram: t.me/bnull

if __name__ == '__main__':
    _default_clients['ANDROID_MUSIC'] = _default_clients['ANDROID_CREATOR']

    root = Tk()
    root.iconbitmap(resource_path('images/app_icon.ico'))
    app = App(root)
    root.mainloop()
