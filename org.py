# import dependencies
import os
from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep
import shutil
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler


# folder to sort and folders to sort into
source_dir = "/Users/josephmonahan/Downloads"
dest_dir_sfx = "/Users/josephmonahan/Desktop/Sound"
dest_dir_music = "/Users/josephmonahan/Desktop/Sound/music"
dest_dir_video = "/Users/josephmonahan/Desktop/VideoDownloads"
dest_dir_image = "/Users/josephmonahan/Desktop/ImageDownloads"
dest_dir_documents = "/Users/josephmonahan/Documents"
print('yes1')

#define file types into categories
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", 
".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw", 
".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf",
".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]

video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]

audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]

document_extensions = [".csv", ".doc", ".docx", ".odt",
".pdf", ".xls", ".xlsx", ".ppt", ".pptx", ".txt"]
print('yes2')

def makeUnique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    # * IF FILE EXISTS, ADDS NUMBER TO THE END OF THE FILENAME
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name



def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = makeUnique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    else:
        print(name)
        move("/Users/josephmonahan/Downloads/"+name, dest)
        

class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with os.scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                print(name)
                self.check_audio_files(entry, name)
                print('booyah')
                self.check_video_files(entry, name)
                self.check_image_files(entry, name)
                self.check_document_files(entry, name)

    def check_audio_files(self, entry, name):
        print('audio')  # * Checks all Audio Files
        for audio_extension in audio_extensions:
            print('audio2')
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                print('audio3')
                if entry.stat().st_size < 10_000_000 or "SFX" in name:  # ? 10Megabytes
                    print('audio4')
                    dest = dest_dir_sfx
                else:
                    dest = dest_dir_music
                    print(name + 'yesyes')
                move_file(dest, entry, name)
                logging.info(f"Moved audio file: {name}")

    def check_video_files(self, entry, name):
        print('video')  # * Checks all Video Files
        for video_extension in video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                move_file(dest_dir_video, entry, name)
                logging.info(f"Moved video file: {name}")

    def check_image_files(self, entry, name):
        print('image')  # * Checks all Image Files
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                move_file(dest_dir_image, entry, name)
                logging.info(f"Moved image file: {name}")

    def check_document_files(self, entry, name):
        print('doc')  # * Checks all Document Files
        for documents_extension in document_extensions:
            if name.endswith(documents_extension) or name.endswith(documents_extension.upper()):
                print('yesyesno')
                move_file(dest_dir_documents, entry, name)
                print('no')
                logging.info(f"Moved document file: {name}")






if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()