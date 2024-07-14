import os
import threading
from tkinter import Tk, Entry, Button, Label, Listbox, Scrollbar, END, DISABLED, NORMAL, Text, Toplevel, Radiobutton, \
    StringVar, MULTIPLE, messagebox, Scale, Menu, PhotoImage

from src.downloader import download_video_audio, download_playlist, multi_download_video_streams, \
    multi_download_audio_streams
from src.translations import translations
from src.utils import is_valid_url, log_status, resource_path


# Andrey Kuzmichev
# Telegram: t.me/bnull

class App:
    def __init__(self, master):
        self.master = master
        self.master.title('YouTube Downloader GUI')

        self.translations = translations

        self.lang = StringVar(value='ru')

        self.menu = Menu(master)
        self.master.config(menu=self.menu)
        self.language_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label=self.translations[self.lang.get()]['language'], menu=self.language_menu)

        self.russia_flag = PhotoImage(file=resource_path('images/russia.png')).subsample(10, 10)
        self.language_menu.add_radiobutton(label='Русский', image=self.russia_flag, compound='left',
                                           value='ru', variable=self.lang, command=self.set_language)
        self.language_menu.entryconfig('Русский', state=DISABLED if self.lang.get() == 'ru' else NORMAL)

        self.language_menu.add_radiobutton(label='English', image=self.russia_flag, compound='left',
                                           value='en', variable=self.lang, command=self.set_language)

        self.label = Label(master, text=self.translations[self.lang.get()]['enter_url'])
        self.label.pack()

        self.url_entry = Entry(master, width=50)
        self.url_entry.pack()

        self.label_path = Label(master, text=self.translations[self.lang.get()]['enter_path'])
        self.label_path.pack()

        self.path_entry = Entry(master, width=50)
        self.path_entry.pack()

        self.label_workers = Label(master, text=self.translations[self.lang.get()]['choose_workers'])
        self.label_workers.pack()

        self.scale_workers = Scale(master, from_=1, to=10, orient='horizontal', length=200)
        self.scale_workers.pack()

        self.download_choice = StringVar(value='both')

        self.video_radiobutton = Radiobutton(master, text=self.translations[self.lang.get()]['download_video'],
                                             variable=self.download_choice,
                                             value='video')
        self.video_radiobutton.pack()

        self.audio_radiobutton = Radiobutton(master, text=self.translations[self.lang.get()]['download_audio'],
                                             variable=self.download_choice,
                                             value='audio')
        self.audio_radiobutton.pack()

        self.both_radiobutton = Radiobutton(master, text=self.translations[self.lang.get()]['download_both'],
                                            variable=self.download_choice, value='both')
        self.both_radiobutton.pack()

        self.download_button = Button(master, text=self.translations[self.lang.get()]['download'],
                                      command=self.start_download)
        self.download_button.pack()

        self.copyright_label = Label(master, text=self.translations[self.lang.get()]['copyright'], fg='grey',
                                     font=('Arial', 8))
        self.copyright_label.pack(pady=(10, 0))

        self.log_text = None
        self.log_window = None
        self.open_log_window()

    def set_language(self):
        lang = self.lang.get()

        self.menu.entryconfig(1, label=self.translations[lang]['language'])
        self.language_menu.entryconfig('Русский', state=DISABLED if lang == 'ru' else NORMAL)
        self.language_menu.entryconfig('English', state=DISABLED if lang == 'en' else NORMAL)

        self.label.config(text=self.translations[lang]['enter_url'])
        self.label_path.config(text=self.translations[lang]['enter_path'])
        self.label_workers.config(text=self.translations[lang]['choose_workers'])
        self.video_radiobutton.config(text=self.translations[lang]['download_video'])
        self.audio_radiobutton.config(text=self.translations[lang]['download_audio'])
        self.both_radiobutton.config(text=self.translations[lang]['download_both'])
        self.download_button.config(text=self.translations[lang]['download'])
        self.copyright_label.config(text=self.translations[lang]['copyright'])

        if self.log_window is not None:
            self.log_window.title(self.translations[lang]['logs_title'])
            clear_button = self.log_window.children['!button']
            clear_button.config(text=self.translations[lang]['clear_logs'])

    def open_log_window(self):
        if self.log_window is not None:
            self.log_window.lift()

            return

        self.log_window = Toplevel(self.master)
        self.log_window.iconbitmap(resource_path('images/app_icon.ico'))
        self.log_window.title(self.translations[self.lang.get()]['logs_title'])
        self.log_window.protocol('WM_DELETE_WINDOW', self.close_main_window)

        self.log_text = Text(self.log_window, height=20, width=60, state=DISABLED)
        self.log_text.pack()

        clear_button = Button(self.log_window, text=self.translations[self.lang.get()]['clear_logs'],
                              command=self.clear_logs)
        clear_button.pack()

    def close_main_window(self):
        if self.log_window is not None:
            self.log_window.destroy()

        self.master.destroy()

    def clear_logs(self):
        self.log_text.config(state=NORMAL)
        self.log_text.delete(1.0, END)
        self.log_text.config(state=DISABLED)

    def start_download(self):
        input_url = self.url_entry.get()
        base_path = self.path_entry.get()
        max_workers = self.scale_workers.get()

        if not input_url or not is_valid_url(input_url):
            messagebox.showerror(self.translations[self.lang.get()]['error'],
                                 self.translations[self.lang.get()]['enter_valid_url'])

            return

        if not base_path or not os.path.exists(base_path):
            messagebox.showerror(self.translations[self.lang.get()]['error'],
                                 self.translations[self.lang.get()]['enter_valid_path'])

            return

        self.download_button.config(state=DISABLED)

        if 'playlist' in input_url:
            threading.Thread(target=download_playlist, args=(input_url, base_path, max_workers, self)).start()
        else:
            threading.Thread(target=download_video_audio, args=(input_url, base_path, max_workers, self)).start()

        self.download_button.config(state=NORMAL)

    def enable_download_button(self):
        self.download_button.config(state=NORMAL)

    def choose_video_streams(self, video_streams, output_path, max_workers, video_title, log_uid):
        choice_window = Tk()
        choice_window.geometry('350x400')
        choice_window.iconbitmap(resource_path('images/app_icon.ico'))
        choice_window.title(self.translations[self.lang.get()]['choose_video_streams'].format(video_title))

        label = Label(choice_window, text=self.translations[self.lang.get()]['select_video_streams'])
        label.pack()

        scrollbar = Scrollbar(choice_window)
        scrollbar.pack(side='right', fill='y')

        listbox = Listbox(choice_window, selectmode=MULTIPLE, yscrollcommand=scrollbar.set)
        listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=listbox.yview)

        for i, stream in enumerate(video_streams):
            listbox.insert(END, f"{i + 1}: {stream.mime_type}, resolution: {stream.resolution}")

        def on_closing():
            chosen_indices = listbox.curselection()

            if chosen_indices:
                ask_cancel = messagebox.askokcancel(
                    self.translations[self.lang.get()]['video_audio_cancel_title'],
                    self.translations[self.lang.get()]['video_audio_cancel_description'],
                    parent=choice_window
                )

                if ask_cancel:
                    log_status(self, self.translations[self.lang.get()]['video_streams_canceled'], log_uid)
                    choice_window.destroy()
            else:
                log_status(self, self.translations[self.lang.get()]['video_streams_canceled'], log_uid)
                choice_window.destroy()

        choice_window.protocol('WM_DELETE_WINDOW', on_closing)

        def on_confirm():
            chosen_indices = listbox.curselection()
            choice_window.destroy()

            log_status(self, self.translations[self.lang.get()]['choose_video_streams_completed'], log_uid)

            threading.Thread(
                target=multi_download_video_streams,
                args=(video_streams, chosen_indices, output_path, max_workers, log_uid, self)
            ).start()

        confirm_button = Button(choice_window, text=self.translations[self.lang.get()]['confirm'], command=on_confirm)
        confirm_button.pack()

        choice_window.mainloop()

    def choose_audio_streams(self, audio_streams, output_path, max_workers, video_title, log_uid):
        choice_window = Tk()
        choice_window.geometry('350x400')
        choice_window.iconbitmap(resource_path('images/app_icon.ico'))
        choice_window.title(self.translations[self.lang.get()]['choose_audio_streams'].format(video_title))

        label = Label(choice_window, text=self.translations[self.lang.get()]['select_audio_streams'])
        label.pack()

        scrollbar = Scrollbar(choice_window)
        scrollbar.pack(side='right', fill='y')

        listbox = Listbox(choice_window, selectmode=MULTIPLE, yscrollcommand=scrollbar.set)
        listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=listbox.yview)

        for i, stream in enumerate(audio_streams):
            listbox.insert(END, f"{i + 1}: {stream.mime_type}, bitrate: {stream.abr}")

        def on_closing():
            chosen_indices = listbox.curselection()

            if chosen_indices:
                ask_cancel = messagebox.askokcancel(
                    self.translations[self.lang.get()]['video_audio_cancel_title'],
                    self.translations[self.lang.get()]['video_audio_cancel_description'],
                    parent=choice_window
                )

                if ask_cancel:
                    log_status(self, self.translations[self.lang.get()]['audio_streams_canceled'], log_uid)
                    choice_window.destroy()
            else:
                log_status(self, self.translations[self.lang.get()]['audio_streams_canceled'], log_uid)
                choice_window.destroy()

        choice_window.protocol('WM_DELETE_WINDOW', on_closing)

        def on_confirm():
            chosen_indices = listbox.curselection()
            choice_window.destroy()

            log_status(self, self.translations[self.lang.get()]['choose_audio_streams_completed'], log_uid)

            threading.Thread(
                target=multi_download_audio_streams,
                args=(audio_streams, chosen_indices, output_path, max_workers, log_uid, self)
            ).start()

        confirm_button = Button(choice_window, text=self.translations[self.lang.get()]['confirm'], command=on_confirm)
        confirm_button.pack()

        choice_window.mainloop()
