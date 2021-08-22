import os
import time
import shutil
import random
import requests
from instabot import Bot
from config import INST_USERNAME, INST_PASSWORD, POST_IN_DAY


test_list = []


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
    Удаление фотографии из директории photos по названию фотографии
    :param image_name: название фотографии
    """
    image = os.path.join(os.getcwd(), "photos", image_name)
    if os.path.exists(image):
        os.remove(image)


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


def get_len_images() -> str:
    """
    Получить количество всех сохраненных фотографий в директории photos и сколько дней они будут публиковаться
    :return: количество всех сохраненных фотографий в директории photos и сколько дней они будут публиковаться
    """
    path = os.path.join(os.getcwd(), "photos")
    images_len = len(os.listdir(path))
    try:
        posts_day_count = images_len / POST_IN_DAY
    except ZeroDivisionError:
        posts_day_count = 0
    text = f"Всего: {images_len} фотографий\n" \
           f"Будет публиковаться: {posts_day_count} дней"
    return text


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
    if media["media_type"] == 2:
        return
    if "image_versions2" in media.keys():
        url = media["image_versions2"]["candidates"][0]["url"]
        response = requests.get(url)
        image_name = os.path.join("photos", filename + ".jpg")
        with open(image_name, "wb") as f:
            response.raw.decode_content = True
            f.write(response.content)
    elif "carousel_media" in media.keys():
        for i, element in enumerate(media["carousel_media"]):
            if element['media_type'] != 2:
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
    check_and_create_folder('photos')
    twenty_last_medias = my_bot.get_total_user_medias(nickname)
    for i, media_id in enumerate(twenty_last_medias):
        download_photo_by_media_id(my_bot, media_id, filename=nickname + str(i))


def download_photos_by_url(my_bot: object, url: str) -> None:
    """
    Скачать фото по ссылке на пост в инстаграмме
    :param my_bot: класс Bot из библиотеки instabot
    :param url: ссылка на пост в инстаграмме
    """
    check_and_create_folder('photos')
    # по url получаем id поста
    media_id = my_bot.get_media_id_from_link(url)
    filename = "my_choice" + str(time.time()).replace('.', '')
    download_photo_by_media_id(my_bot, media_id, filename=filename)

# автовыкладывание
# комментирование
# хеширование и валидация
