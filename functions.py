import os
import time
import shutil
import random
import imagehash
import requests
import config
from PIL import Image
from typing import Tuple
from potoki import create_threads
from tqdm import tqdm as loading_bar
from json_classes import ImagesHashes


def create_base_directory() -> None:
    """
    Проверяет и создает базовые директории, если таковые отсутствуют (при старте проекта)
    """
    for el in config.BASE_FOLDERS_NAMES:
        check_and_create_folder(el)


def clean_up(config_dir_name: str = "config") -> None:
    """
    Удаляет ненужные директории при инициализации подключения, иначе подключение не получится
    :param config_dir_name: по умолчанию удаляет папку config, иначе не произойдет подключение к API инстаграмм
    """
    directory = os.path.join(os.getcwd(), config_dir_name)
    if os.path.exists(directory):
        try:
            shutil.rmtree(directory)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))


def check_and_create_folder(folder_name: str) -> None:
    """
    Проверяет, существует ли директория, если нет - создает
    :param folder_name: Название диретории
    """
    directory = os.path.join(os.getcwd(), folder_name)
    if not os.path.exists(directory):
        os.mkdir(directory)


def random_choice_image() -> str:
    """
    Выбрать случайное имя фотографии из директории photos
    :return: случайно выбранное имя
    """
    ...
    messages_ids = ...
    image_name = random.choice(messages_ids)
    return image_name


def download_photo_by_media_id(my_bot: object, media_id: int, filename: str, media_numbers: list,
                               folder: str = config.PHOTO_SAVE_FOLDER_NAME) -> None:
    """
    :param my_bot: класс Bot из библиотеки instabot
    :param media_id: id поста, в которой возможно содержится фотография или крусель из фотографий
    :param filename: название, что будет приствоено фотографии
    :param media_numbers: список номеров media для загрузки из карусели
    :param folder: Хранилище фотографий
    media_type:
    1 - фото
    2 - видео
    8 - карусель
    """
    media = my_bot.get_media_info(media_id)[0]
    if "image_versions2" in media.keys() and media["media_type"] != 2:
        url = media["image_versions2"]["candidates"][0]["url"]
        response = requests.get(url)
        content = response.content
        if not image_validation(content):
            image_name = os.path.join(folder, filename + ".jpg")
            with open(image_name, "wb") as f:
                response.raw.decode_content = True
                f.write(content)
    elif "carousel_media" in media.keys():
        for i, element in enumerate(media["carousel_media"]):
            if i in media_numbers and element['media_type'] != 2:
                url = element['image_versions2']["candidates"][0]["url"]
                response = requests.get(url)
                content = response.content
                if not image_validation(content):
                    image_name = os.path.join(folder, filename + "_" + str(i) + ".jpg")
                    with open(image_name, "wb") as f:
                        response.raw.decode_content = True
                        f.write(content)


def download_all_user_photos(my_bot: object, nickname: str, start: int, stop: int) -> None:
    """
    Получить все фотографии пользователя
    :param my_bot: класс Bot из библиотеки instabot
    :param nickname: имя пользователя в инстаграмме
    :param start: начать скачивание с media под номером n
    :param stop: закончить скачивание на media под номером n
    """
    all_medias = my_bot.get_total_user_medias(nickname)
    create_threads(my_bot, all_medias, nickname, start=start, stop=stop)


def download_last_user_photos(my_bot: object, nickname: str, start: int = 0, stop: int = 10000) -> None:
    """
    Получить 20 последних фотографии пользователя
    :param my_bot: класс Bot из библиотеки instabot
    :param nickname: имя пользователя в инстаграмме
    :param start: начать скачивание с media под номером n
    :param stop: закончить скачивание на media под номером n
    """
    twenty_last_medias = my_bot.get_user_medias(nickname, filtration=None)
    create_threads(my_bot, twenty_last_medias, nickname, start=start, stop=stop)


def download_photos_by_url(my_bot: object, url: str, media_numbers: list) -> str:
    """
    Скачать фото по ссылке на пост в инстаграмме
    :param my_bot: класс Bot из библиотеки instabot
    :param url: ссылка на пост в инстаграмме
    :param media_numbers: список номеров media для загрузки из карусели
    """
    # по url получаем id поста
    media_id = my_bot.get_media_id_from_link(url)
    filename = "my_choice" + str(time.time()).replace('.', '')
    download_photo_by_media_id(my_bot, media_id, filename, media_numbers)
    return filename


def get_nickname_and_download_limits(message: str) -> tuple:
    """
    Разбить сообщение на никнейм, начало загрузки и конец загрузки
    :param message: Сообщение, присланное боту
    :return: кортеж из никнейма, начала загрузки и конца загрузки
    """
    res = message.replace('\n', '')
    res = res.split()
    res = [x.strip() for x in res]
    if len(res) == 1:
        nickname_and_limits = (res[0], 0, 10000)
    elif len(res) == 2:
        nickname_and_limits = (res[0], res[1], 10000)
    elif len(res) == 3:
        nickname_and_limits = (res[0], res[1], res[2])
    else:
        nickname_and_limits = (res[0], res[1], res[2])
    return nickname_and_limits


def get_post_url_and_media_numbers(message: str) -> Tuple[str, list]:
    """
    Разбить сообщение на url поста и список из номеров необходимых медиа из карусели
    :param message: Сообщение, присланное боту
    :return: кортеж из url поста и списока из номеров необходимых медиа из карусели
    """
    res = message.replace('\n', '')
    res = res.split()
    res = [x.strip() for x in res]
    post_url, *media_numbers = res
    if media_numbers:
        media_numbers = [int(x) - 1 for x in media_numbers]
    else:
        media_numbers = list(range(20))
    url_and_numbers = (post_url, media_numbers)
    return url_and_numbers


def paste_watermark(image_name) -> None:
    directory = os.path.join(os.getcwd(), config.PHOTO_SAVE_FOLDER_NAME, image_name)

    image = Image.open(directory)

    watermark = Image.open('watermark.png')
    watermark_size_x = int(image.size[0] / 3)
    watermark_size_y = int(watermark_size_x / 4.46)
    new_watermark = watermark.resize((watermark_size_x, watermark_size_y), Image.ANTIALIAS)

    image.paste(new_watermark, (image.size[0] - watermark_size_x, image.size[1] - watermark_size_y), new_watermark)
    image.save(directory, "JPEG", optimize=True)


def paste_watermarks_to_images(images_names: list) -> None:
    for image in loading_bar(images_names, desc='Установка водяных знаков на фото'):
        paste_watermark(image)
