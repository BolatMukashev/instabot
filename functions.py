import os
import shutil
import requests
import time
from instabot import Bot
from config import INST_USERNAME, INST_PASSWORD


def connect() -> object:
    """
    Осуществляем вход в инстаграм по логину и паролю
    :return: объект Bot из библиотеки instabot
    """
    clean_up()
    bot = Bot()
    bot.login(username=INST_USERNAME, password=INST_PASSWORD)
    return bot


def clean_up(*args: str, config_dir_name: str = "config") -> None:
    """
    Удаляет ненужные директории при инициализации подключения, иначе подключение не получится
    А так же удаляет директории по запросу
    :param args: удаляет директории по запросу, прописывать названии ненужных дирректорий
    :param config_dir_name: по умолчанию удаляет папку config, иначе не произойдет подключение к API инстаграмм
    """
    if args:
        for nickname in args:
            directory = os.path.join(os.getcwd(), "photos", nickname)
            if os.path.exists(directory):
                try:
                    shutil.rmtree(directory)
                except OSError as e:
                    print("Error: %s - %s." % (e.filename, e.strerror))
    else:
        directory = os.path.join(os.getcwd(), config_dir_name)
        if os.path.exists(directory):
            try:
                shutil.rmtree(directory)
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))


def download_photo_by_media_id(my_bot: object, media_id: int, filename: str) -> None:
    """
    :param my_bot: класс Bot из библиотеки instabot
    :param media_id: id поста, в которой возможно содержится фотография или крусель из фотографий
    :param filename: название, что будет приствоено фотографии
    """
    media = my_bot.get_media_info(media_id)[0]
    if "image_versions2" in media.keys():
        url = media["image_versions2"]["candidates"][0]["url"]
        response = requests.get(url)
        image_name = os.path.join("photos", filename + ".jpg")
        with open(image_name, "wb") as f:
            response.raw.decode_content = True
            f.write(response.content)
    elif "carousel_media" in media.keys():
        for i, element in enumerate(media["carousel_media"]):
            url = element['image_versions2']["candidates"][0]["url"]
            response = requests.get(url)
            image_name = os.path.join("photos", filename + "_" + str(i) + ".jpg")
            with open(image_name, "wb") as f:
                response.raw.decode_content = True
                f.write(response.content)


def download_all_user_photos(my_bot: object, nickname: str) -> None:
    """
    Получить все фотографии пользователя
    :param my_bot: класс Bot из библиотеки instabot
    :param nickname: имя пользователя в инстаграмме и имя директории, куда будут сохранены фотографии
    """
    twenty_last_medias = my_bot.get_total_user_medias(nickname)
    for i, media_id in enumerate(twenty_last_medias):
        download_photo_by_media_id(my_bot, media_id, filename=nickname + str(i))


def download_photos_by_url(my_bot: object, url: str) -> None:
    """
    Скачать фото по ссылке на пост в инстаграмме
    :param my_bot: класс Bot из библиотеки instabot
    :param url: ссылка на пост в инстаграмме
    """
    # по url получаем id поста
    media_id = my_bot.get_media_id_from_link(url)
    filename = "my_choice" + str(time.time()).replace('.', '')
    download_photo_by_media_id(my_bot, media_id, filename=filename)
