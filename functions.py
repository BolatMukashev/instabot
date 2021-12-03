import os
import random
from aiogram.types import InputMediaPhoto
import config
from json_classes import PhotosData


def create_base_directory() -> None:
    """
    Проверяет и создает базовые директории, если таковые отсутствуют (при старте проекта)
    """
    for el in config.BASE_FOLDERS_NAMES:
        check_and_create_folder(el)


def check_and_create_folder(folder_name: str) -> None:
    """
    Проверяет, существует ли директория, если нет - создает
    :param folder_name: Название диретории
    """
    directory = os.path.join(os.getcwd(), folder_name)
    if not os.path.exists(directory):
        os.mkdir(directory)


def get_number_of_images():
    data = PhotosData.get_data_from_json_file()
    keys = data.keys()
    return len(keys)


def get_n_random_message_id_from_data(count: int) -> list:
    data = PhotosData.get_data_from_json_file()
    keys = data.keys()
    return random.sample(keys, count)


def get_photos(keys: list, caption: str) -> list:
    data = PhotosData.get_data_from_json_file()
    photos = [InputMediaPhoto(data[keys[0]], caption)]
    for el in keys[1:]:
        photos.append(InputMediaPhoto(data[el], ''))
        return photos
