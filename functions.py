import os
import time
import json
import shutil
import random
import bot_config
import hashlib
import requests
from typing import Union
from instabot import Bot


test_list = []


def connect() -> object:
    """
    Осуществляем вход в инстаграм по логину и паролю
    :return: объект Bot из библиотеки instabot
    """
    clean_up()
    bot = Bot()
    bot.login(username=bot_config.INST_USERNAME, password=bot_config.INST_PASSWORD)
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


def delete_image(image_name: str) -> None:
    """
    Удалить фотографию из директории photos по названию этой фотографии
    :param image_name: название фотографии
    """
    image = os.path.join(os.getcwd(), "photos", image_name)
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


def delete_all_images() -> None:
    """
    Удаление всех фотографии из директории photos
    Удаляет директорию photos и создает заново пустую директорию
    """
    directory = os.path.join(os.getcwd(), "photos")
    if os.path.exists(directory):
        try:
            shutil.rmtree(directory)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
    check_and_create_folder('photos')


def get_all_images_names() -> list:
    """
    Получить список имен всех фотографий в директории photos
    :return: список имен
    """
    path = os.path.join(os.getcwd(), "photos")
    images_names_list = os.listdir(path)
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


def get_len_images() -> tuple:
    """
    Получить количество всех сохраненных фотографий в директории photos и сколько дней они будут публиковаться
    :return: количество всех сохраненных фотографий в директории photos и сколько дней они будут публиковаться
    """
    path = os.path.join(os.getcwd(), "photos")
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


def download_photo_by_media_id(my_bot: object, media_id: int, filename: str) -> None:
    """
    :param my_bot: класс Bot из библиотеки instabot
    :param media_id: id поста, в которой возможно содержится фотография или крусель из фотографий
    :param filename: название, что будет приствоено фотографии
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
            image_name = os.path.join("photos", filename + ".jpg")
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
                    image_name = os.path.join("photos", filename + "_" + str(i) + ".jpg")
                    with open(image_name, "wb") as f:
                        response.raw.decode_content = True
                        f.write(content)


def download_all_user_photos(my_bot: object, nickname: str) -> None:
    """
    Получить все фотографии пользователя
    :param my_bot: класс Bot из библиотеки instabot
    :param nickname: имя пользователя в инстаграмме и имя директории, куда будут сохранены фотографии
    """
    twenty_last_medias = my_bot.get_total_user_medias(nickname)
    for i, media_id in enumerate(twenty_last_medias):
        download_photo_by_media_id(my_bot, media_id, filename=nickname + str(i))


def update_all_users_photos(my_bot: object) -> int:
    """
    Скачать новые фотографии сохраненных пользователей (в базе никнеймов)
    :param my_bot: класс Bot из библиотеки instabot
    """
    count_photos_in_start, _ = get_len_images()
    users_nicknames = get_data_from_json_file(bot_config.JSON_FILE_WITH_NICKNAMES)
    for nickname in users_nicknames:
        download_all_user_photos(my_bot, nickname)
    count_photos_in_the_end, _ = get_len_images()
    difference = count_photos_in_start - count_photos_in_the_end
    return difference


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


def get_image_hash(response: object) -> str:
    """
    Получаем хэш фотографии из объекта response
    :param response: объект response
    :return: хэш фотографии
    """
    byte_view_of_the_photo = response.__repr__().encode('utf-8')
    image_hash = hashlib.md5(byte_view_of_the_photo).hexdigest()
    return image_hash


def check_data_in_json_file(json_file_name: str, required_data: str) -> Union[bool, None]:
    """
    Проверка наличия искомых данных в json файле
    :param json_file_name: Имя json файла, где осуществляется поиск
    :param required_data: искомое значение
    :return: True или None
    """
    data = get_data_from_json_file(json_file_name)
    if required_data in data:
        return True


def image_validation(response: object) -> bool:
    """
    Проверка фотографии в базе. Если есть - True, если нет - добавить хэш в базу и вернуть False
    :param response: объект response
    :return: True или False
    """
    image_hash = get_image_hash(response)
    check_result = bool(check_data_in_json_file(bot_config.HASH_JSON_FILE_NAME, image_hash))
    if check_result is False:
        insert_new_data_in_json_file(bot_config.HASH_JSON_FILE_NAME, image_hash)
    return check_result


def create_json_file(json_file_name: str, new_data: any) -> None:
    """
    Создать json файл
    :param json_file_name: Имя файла
    :param new_data: Новые данные
    """
    directory = os.path.join(os.getcwd(), 'db', json_file_name)
    with open(directory, 'w', encoding='utf-8') as json_file:
        json.dump(new_data, json_file, ensure_ascii=False)


def get_data_from_json_file(json_file_name: str) -> any:
    """
    Получить данные из json файла. Если файла отсутствует - создает новый файл
    :param json_file_name: Имя файла
    :return: Данные из json файла
    """
    directory = os.path.join(os.getcwd(), 'db', json_file_name)
    if not os.path.exists(directory):
        create_json_file(json_file_name, [])
    with open(directory, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data


def insert_new_data_in_json_file(json_file_name: str, new_data: str) -> None:
    """
    Перезаписать json файл с новыми данными
    :param json_file_name: Имя файла
    :param new_data: Новые данные
    """
    data = get_data_from_json_file(json_file_name)
    data.append(new_data)
    create_json_file(json_file_name, data)


# фронт работ:
# автовыкладывание
# групповое выкладывание
# комментирование
# классы json и т.д.
