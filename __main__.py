from tkinter import Tk

from pytube.innertube import _default_clients

from src.gui import App
from src.utils import resource_path

# Andrey Kuzmichev
# Telegram: t.me/bnull

if __name__ == '__main__':
    _default_clients['ANDROID_MUSIC'] = _default_clients['WEB']

    root = Tk()
    root.iconbitmap(resource_path('images/app_icon.ico'))
    app = App(root)
    root.mainloop()
