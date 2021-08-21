import os
import shutil
import requests
from instabot import Bot
from config import INST_USERNAME, INST_PASSWORD


def connect() -> object:
    """
    Осуществляем вход в инстаграм по логину и паролю
    :return: объект Bot из библиотеки instabot
    """
    bot = Bot()
    bot.login(username=INST_USERNAME, password=INST_PASSWORD)
    return bot


def clean_up(*args: str, dir_name: str = "config") -> None:
    """
    Удаляет ненужные директории при инициализации подключения, иначе подключение не получится
    А так же удаляет директории по запросу
    :param args: удаляет директории по запросу, прописывать названии ненужных дирректорий
    :param dir_name: по умолчанию удаляет папку config, иначе не произойдет подключение к API инстаграмм
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
        directory = os.path.join(os.getcwd(), dir_name)
        if os.path.exists(directory):
            try:
                shutil.rmtree(directory)
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))


def create_new_directory(dir_name: str) -> None:
    """
    Проверить и создать новую директорию
    :param dir_name: название директории
    """
    directory = os.path.join('photos', dir_name)
    if not os.path.exists(directory):
        os.mkdir(directory)


def download_photo_by_media_id(my_bot: object, media_id: int, filename: str, directory_name: str) -> None:
    """
    :param my_bot: класс Bot из библиотеки instabot
    :param media_id: id поста, в которой возможно содержится фотография или крусель из фотографий
    :param filename: название, что будет приствоено фотографии
    :param directory_name: директория, куда будут сохранены фотографии
    :return:
    """
    media = my_bot.get_media_info(media_id)[0]
    if "image_versions2" in media.keys():
        url = media["image_versions2"]["candidates"][0]["url"]
        response = requests.get(url)
        with open("photos" + "/" + directory_name + "/" + filename + ".jpg", "wb") as f:
            response.raw.decode_content = True
            f.write(response.content)
    elif "carousel_media" in media.keys():
        for e, element in enumerate(media["carousel_media"]):
            url = element['image_versions2']["candidates"][0]["url"]
            response = requests.get(url)
            with open("photos" + "/" + directory_name + "/" + filename + str(e) + ".jpg", "wb") as f:
                response.raw.decode_content = True
                f.write(response.content)


def get_all_photos(my_bot: object, nickname: str) -> None:
    """
    Получить все фотографии пользователя
    :param my_bot: класс Bot из библиотеки instabot
    :param nickname: имя пользователя в инстаграмме и имя директории, куда будут сохранены фотографии
    """
    twenty_last_medias = my_bot.get_total_user_medias(nickname)
    os.mkdir("photos" + "/" + nickname)
    for e, media_id in enumerate(twenty_last_medias):
        download_photo_by_media_id(my_bot, media_id, filename="img_" + str(e), directory_name=nickname)


def get_photo_by_url(my_bot: object, url: str) -> None:
    """
    Скачать фото по ссылке на пост в инстаграмме
    :param my_bot: класс Bot из библиотеки instabot
    :param url: ссылка на пост в инстаграмме
    """
    # по url получаем id поста
    media_id = my_bot.get_media_id_from_link(url)
    create_new_directory("another")
    download_photo_by_media_id(my_bot, media_id, filename="test", directory_name="another")
