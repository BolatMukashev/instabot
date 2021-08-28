import os
import time
import shutil
import random
import hashlib
import requests
import bot_config
from PIL import Image
from instabot import Bot
from json_classes import ImagesHashes, Nicknames
from potoki import create_threads

test_list = []


def connect() -> object:
    """
    Осуществляем вход в инстаграм по логину и паролю
    :return: объект Bot из библиотеки instabot
    """
    clean_up()
    bot = Bot()
    bot.login(username=bot_config.INST_USERNAME, password=bot_config.INST_PASSWORD, ask_for_code=True)
    return bot


def create_base_directory() -> None:
    """
    Проверяет и создает базовые директории, если таковые отсутствуют (при старте проекта)
    """
    for el in bot_config.BASE_FOLDER_NAMES:
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


def delete_image(image_name: str, folder: str = bot_config.PHOTO_SAVE_FOLDER_NAME) -> None:
    """
    Удалить фотографию из директории photos по названию этой фотографии
    :param folder: Хранилище фотографий
    :param image_name: название фотографии
    """
    image = os.path.join(os.getcwd(), folder, image_name)
    if os.path.exists(image):
        try:
            os.remove(image)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))


def delete_images(image_names: list) -> None:
    """
    Удалить несколько фотографии из директории photos по названию фотографии
    :param image_names: список с названиями фотографии
    """
    for image_name in image_names:
        delete_image(image_name)


def delete_all_images(folder: str = bot_config.PHOTO_SAVE_FOLDER_NAME) -> None:
    """
    Удаление всех фотографии из директории photos
    Удаляет директорию photos и создает заново пустую директорию
    """
    directory = os.path.join(os.getcwd(), folder)
    if os.path.exists(directory):
        try:
            shutil.rmtree(directory)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
    check_and_create_folder('photos')


def image_name_validation(image_name):
    """
    Проверка разрешения
    :param image_name: название фотографии
    :return: название фотографии если разрешение ".jpg"
    """
    if image_name[-4:] == '.jpg':
        return image_name


def get_all_images_names(folder: str = bot_config.PHOTO_SAVE_FOLDER_NAME) -> list:
    """
    Получить список имен всех фотографий в директории photos
    :return: список имен
    """
    path = os.path.join(os.getcwd(), folder)
    images_names_list = os.listdir(path)
    images_names_list = list(filter(image_name_validation, images_names_list))
    return images_names_list


def get_random_images_names(count: int) -> list:
    """
    Получить список имен случайно отобранных фотографий в директории photos
    :count: Количество имен
    :return: список из n имен
    """
    images_names_list = []
    all_images_names_list = get_all_images_names()
    while len(images_names_list) < count:
        image_name = random.choice(all_images_names_list)
        if image_name not in images_names_list:
            images_names_list.append(image_name)
    return images_names_list


def get_number_of_images(folder: str = bot_config.PHOTO_SAVE_FOLDER_NAME) -> tuple:
    """
    Получить количество всех сохраненных фотографий в директории photos и сколько дней они будут публиковаться
    :return: количество всех сохраненных фотографий в директории photos и сколько дней они будут публиковаться
    """
    path = os.path.join(os.getcwd(), folder)
    images_len = len(os.listdir(path))
    try:
        posts_day_count = images_len / bot_config.POST_IN_DAY
    except ZeroDivisionError:
        posts_day_count = 0
    return images_len, posts_day_count


def random_choice_image() -> str:
    """
    Выбрать случайное имя фотографии из директории photos
    :return: случайно выбранное имя
    """
    images_names_list = get_all_images_names()
    image_name = random.choice(images_names_list)
    return image_name


def download_photo_by_media_id(my_bot: object, media_id: int, filename: str,
                               folder: str = bot_config.PHOTO_SAVE_FOLDER_NAME) -> None:
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
            if element['media_type'] != 2:
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


def update_all_users_photos(my_bot: object) -> int:
    """
    Скачать новые фотографии сохраненных пользователей (в базе никнеймов)
    :param my_bot: класс Bot из библиотеки instabot
    """
    count_photos_in_start, _ = get_number_of_images()
    users_nicknames = Nicknames.get_data_from_json_file()
    for nickname in users_nicknames:
        download_last_user_photos(my_bot, nickname)
    count_photos_in_the_end, _ = get_number_of_images()
    difference = count_photos_in_start - count_photos_in_the_end
    return difference


def download_photos_by_url(my_bot: object, url: str) -> str:
    """
    Скачать фото по ссылке на пост в инстаграмме
    :param my_bot: класс Bot из библиотеки instabot
    :param url: ссылка на пост в инстаграмме
    """
    # по url получаем id поста
    media_id = my_bot.get_media_id_from_link(url)
    filename = "my_choice" + str(time.time()).replace('.', '')
    download_photo_by_media_id(my_bot, media_id, filename=filename)
    return filename


def get_image_hash(response: object) -> str:
    """
    Получаем хэш фотографии из объекта response
    :param response: объект response
    :return: хэш фотографии
    """
    byte_view_of_the_photo = response.__repr__().encode('utf-8')
    image_hash = hashlib.md5(byte_view_of_the_photo).hexdigest()
    return image_hash


def image_validation(response: object) -> bool:
    """
    Проверка фотографии в базе. Если есть - True, если нет - добавить хэш в базу и вернуть False
    :param response: объект response
    :return: True или False
    """
    image_hash = get_image_hash(response)
    check_result = bool(ImagesHashes.check_data_in_json_file(image_hash))
    if check_result is False:
        ImagesHashes.insert_new_data_in_json_file(image_hash)
    return check_result


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


def paste_watermark(image_name) -> None:
    directory = os.path.join(os.getcwd(), bot_config.PHOTO_SAVE_FOLDER_NAME, image_name)

    image = Image.open(directory)

    watermark = Image.open('watermark.png')
    watermark_size_x = int(image.size[0] / 3)
    watermark_size_y = int(watermark_size_x / 4.46)
    new_watermark = watermark.resize((watermark_size_x, watermark_size_y), Image.ANTIALIAS)

    image.paste(new_watermark, (image.size[0] - watermark_size_x, image.size[1] - watermark_size_y), new_watermark)
    image.save(directory, "JPEG", optimize=True)


def paste_watermarks_to_images(images_names: list) -> None:
    for image in images_names:
        paste_watermark(image)
