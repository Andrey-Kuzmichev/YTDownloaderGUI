import os
from concurrent.futures import ThreadPoolExecutor

from pytubefix import YouTube, Playlist

from src.utils import log_status, sanitize_filename, generate_short_uid


# Andrey Kuzmichev
# Telegram: t.me/bnull

def download_video_streams(video_streams, idx, output_path, log_uid, gui):
    video_stream = video_streams[idx]
    video_extension = video_stream.mime_type.split('/')[-1]

    log_status(gui, gui.translations[gui.lang.get()]['downloading_video_start'].format(idx + 1), log_uid)

    try:
        video_stream.download(output_path=output_path, filename=f"video_{idx + 1}.{video_extension}")
    except BaseException as error:
        log_status(gui, error.__str__(), log_uid)

        return

    log_status(gui, gui.translations[gui.lang.get()]['downloaded_video_stream'].format(idx + 1), log_uid)


def multi_download_video_streams(video_streams, chosen_indices, output_path, max_workers, log_uid, gui):
    log_status(gui, gui.translations[gui.lang.get()]['downloading_video_streams'], log_uid)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(download_video_streams, video_streams, idx, output_path, log_uid, gui)
                   for idx in chosen_indices]

        for future in futures:
            try:
                future.result()
            except Exception as e:
                log_status(gui, gui.translations[gui.lang.get()]['error_downloading_video_audio_in_pool'].format(e))

    log_status(gui, gui.translations[gui.lang.get()]['video_download_completed'], log_uid)


def download_audio_streams(audio_streams, idx, output_path, log_uid, gui):
    audio_stream = audio_streams[idx]
    audio_extension = audio_stream.mime_type.split('/')[-1]

    log_status(gui, gui.translations[gui.lang.get()]['downloading_audio_start'].format(idx + 1), log_uid)

    try:
        audio_stream.download(output_path=output_path, filename=f"audio_{idx + 1}.{audio_extension}")
    except BaseException as error:
        log_status(gui, error.__str__(), log_uid)

        return

    log_status(gui, gui.translations[gui.lang.get()]['downloaded_audio_stream'].format(idx + 1), log_uid)


def multi_download_audio_streams(audio_streams, chosen_indices, output_path, max_workers, log_uid, gui):
    log_status(gui, gui.translations[gui.lang.get()]['downloading_audio_streams'], log_uid)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(download_audio_streams, audio_streams, idx, output_path, log_uid, gui)
                   for idx in chosen_indices]

        for future in futures:
            try:
                future.result()
            except Exception as e:
                log_status(gui, gui.translations[gui.lang.get()]['error_downloading_video_audio_in_pool'].format(e))

    log_status(gui, gui.translations[gui.lang.get()]['audio_download_completed'], log_uid)


def download_playlist(playlist_url, output_directory, max_workers, gui):
    try:
        playlist = Playlist(playlist_url)
    except BaseException as error:
        log_status(gui, error.__str__())

        return

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(download_video_audio, video_url, output_directory, max_workers, gui)
                   for video_url in playlist.video_urls]

        for future in futures:
            try:
                future.result()
            except Exception as e:
                log_status(gui, gui.translations[gui.lang.get()]['error_downloading_video_audio_in_pool'].format(e))

    gui.enable_download_button()


def download_video_audio(video_url, output_directory, max_workers, gui):
    log_uid = generate_short_uid()

    try:
        yt = YouTube(video_url)
    except BaseException as error:
        log_status(gui, error.__str__())

        return

    video_title = sanitize_filename('{} - {}'.format(yt.author, yt.video_id))
    video_output_path = os.path.join(output_directory, video_title)

    if not os.path.exists(video_output_path):
        os.makedirs(video_output_path)

    log_status(gui, gui.translations[gui.lang.get()]['start_download'], log_uid)

    choice = gui.download_choice.get()

    if choice in ['video', 'both']:
        log_status(gui, gui.translations[gui.lang.get()]['selecting_video_streams'], log_uid)

        try:
            video_streams = yt.streams.filter(only_video=True).order_by('resolution').desc()
        except BaseException as error:
            try:
                os.rmdir(video_output_path)
            except OSError:
                pass

            log_status(gui, error.__str__(), log_uid)

            return

        if video_streams:
            gui.choose_video_streams(video_streams, video_output_path, max_workers, video_title, log_uid)
        else:
            log_status(gui, gui.translations[gui.lang.get()]['no_video_stream'].format(yt.title), log_uid)

    if choice in ['audio', 'both']:
        log_status(gui, gui.translations[gui.lang.get()]['selecting_audio_streams'], log_uid)

        try:
            audio_streams = yt.streams.filter(only_audio=True).order_by('abr').desc()
        except BaseException as error:
            try:
                os.rmdir(video_output_path)
            except OSError:
                pass

            log_status(gui, error.__str__(), log_uid)

            return

        if audio_streams:
            gui.choose_audio_streams(audio_streams, video_output_path, max_workers, video_title, log_uid)
        else:
            log_status(gui, gui.translations[gui.lang.get()]['no_audio_stream'].format(yt.title), log_uid)
