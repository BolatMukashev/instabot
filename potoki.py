import os
import time
import bot_config
from threading import Thread
import requests
import functions

directory = os.path.join(os.getcwd(), bot_config.PHOTO_SAVE_FOLDER_NAME)

images_names = os.listdir(directory)


class MyThread(Thread):
    """
    :param my_bot: класс Bot из библиотеки instabot
    :param media_id: id поста, в которой возможно содержится фотография или крусель из фотографий
    :param filename: название, что будет приствоено фотографии
    :param folder: Хранилище фотографий
    media_type:
    1 - фото
    2 - видео
    8 - карусель
    """
    def __init__(self, my_bot: object, media_id: int, filename: str,
                 folder: str = bot_config.PHOTO_SAVE_FOLDER_NAME):
        """Инициализация потока"""
        Thread.__init__(self)
        self.my_bot = my_bot
        self.media_id = media_id
        self.filename = filename
        self.folder = folder

    def run(self):
        media = self.my_bot.get_media_info(self.media_id)[0]
        if "image_versions2" in media.keys() and media["media_type"] != 2:
            url = media["image_versions2"]["candidates"][0]["url"]
            response = requests.get(url)
            content = response.content
            if not functions.image_validation(content):
                image_name = os.path.join(self.folder, self.filename + ".jpg")
                with open(image_name, "wb") as f:
                    response.raw.decode_content = True
                    f.write(content)
        elif "carousel_media" in media.keys():
            for i, element in enumerate(media["carousel_media"]):
                if element['media_type'] != 2:
                    url = element['image_versions2']["candidates"][0]["url"]
                    response = requests.get(url)
                    content = response.content
                    if not functions.image_validation(content):
                        image_name = os.path.join(self.folder, self.filename + "_" + str(i) + ".jpg")
                        with open(image_name, "wb") as f:
                            response.raw.decode_content = True
                            f.write(content)


def create_threads(my_bot: object, all_medias: list, nickname: str, time_to_sleep: int = bot_config.TIME_TO_SLEEP,
                   start_with: int = bot_config.DOWNLOAD_START_WITH):
    """
    Создаем группу потоков
    time.sleep(3) - без этого параметра instagram кидает бан на час.
    3 секунды - оптимальный вариант
    """
    for i, media_id in enumerate(all_medias):
        if i >= start_with:
            my_thread = MyThread(my_bot, media_id, filename=nickname + "_" + str(i))
            my_thread.start()
            time.sleep(time_to_sleep)
