import os
import random
import re
import string
import sys
from tkinter import END, DISABLED, NORMAL


# Andrey Kuzmichev
# Telegram: t.me/bnull

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', '', filename)


def is_valid_url(url):
    youtube_regex = re.compile(r'^(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+$')

    return youtube_regex.match(url) is not None


def log_status(gui, message, log_uid='root'):
    gui.log_text.config(state=NORMAL)
    gui.log_text.insert(END, f"[{log_uid}] " + message + '\n')
    gui.log_text.see(END)
    gui.log_text.config(state=DISABLED)


def generate_short_uid(length_word=10):
    characters = string.ascii_letters + string.digits

    return ''.join(random.choice(characters) for _ in range(3, length_word))


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath('.')

    return os.path.join(base_path, relative_path.replace('/', '\\'))
