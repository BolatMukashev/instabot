import os
import json
from typing import Union


class JsonFile(object):

    def __init__(self, json_file_name: str):
        """:param json_file_name: Имя файла"""
        self.json_file_name = json_file_name
        self.directory = os.path.join(os.getcwd(), 'db', self.json_file_name)

    def create_json_file(self, new_data: any = None) -> None:
        """
        Создать json файл
        :param new_data: Новые данные
        """
        if new_data is None:
            new_data = []
        with open(self.directory, 'w', encoding='utf-8') as json_file:
            json.dump(new_data, json_file, ensure_ascii=False)

    def search_json_file_and_create(self) -> None:
        """Проверить, существует ли json файл. Если файла отсутствует - создает новый файл"""
        if not os.path.exists(self.directory):
            self.create_json_file()

    def get_data_from_json_file(self) -> any:
        """
        Получить данные из json файла.
        :return: Данные из json файла
        """
        self.search_json_file_and_create()
        with open(self.directory, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            return data

    def insert_new_data_in_json_file(self, new_data: str) -> None:
        """
        Перезаписать json файл с новыми данными
        :param new_data: Новые данные
        """
        data = self.get_data_from_json_file()
        data.append(new_data)
        self.create_json_file(data)

    def check_data_in_json_file(self, required_data: str) -> Union[bool, None]:
        """
        Проверка наличия искомых данных в json файле
        :param required_data: искомое значение
        :return: True или None
        """
        data = self.get_data_from_json_file()
        if required_data in data:
            return True


ImagesHashes = JsonFile("all_images_hashes.json")
Nicknames = JsonFile("nicknames.json")
