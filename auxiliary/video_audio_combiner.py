import os
import subprocess

# Путь к исполняемому файлу FFmpeg. Пример: C:\ffmpeg.exe
ffmpeg_path = r""

# Путь к папке с видео и аудио файлами. Пример: C:\video_audio
video_audio_path = r""

# Получаем список папок внутри video_audio_path
folders = [f.path for f in os.scandir(video_audio_path) if f.is_dir()]

# Обходим каждую папку
for folder in folders:
    # Получаем название папки
    folder_name = os.path.basename(folder)

    # Получаем список видео и аудио файлов внутри папки
    video_files = [f.path for f in os.scandir(folder) if f.is_file() and
                   f.name.startswith("video") and f.name.endswith(".webm")]
    audio_files = [f.path for f in os.scandir(folder) if f.is_file() and
                   f.name.startswith("audio") and f.name.endswith(".webm")]

    # Проверяем, есть ли как минимум один видео и один аудио файл
    if video_files and audio_files:
        # Берем первый видео и первый аудио файл из списка
        video_file = video_files[0]
        audio_file = audio_files[0]

        # Создаем команду FFmpeg
        command = (fr'{ffmpeg_path} -i "{video_file}" -i "{audio_file}" '
                   fr'-c:v copy -c:a copy -metadata:s:a:0 language=rus '
                   fr'"{video_audio_path}\{folder_name}\output_video_with_audio.webm"')

        # Выводим команду в консоль
        subprocess.run(command, shell=True)
