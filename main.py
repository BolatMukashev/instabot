import os
import shutil
import requests
from instabot import Bot
from config import INST_USERNAME, INST_PASSWORD


user_url = "https://www.instagram.com/p/CSwTRIDoJlm/?utm_source=ig_web_copy_linkk"


def connect():
    bot = Bot()
    bot.login(username=INST_USERNAME, password=INST_PASSWORD)
    return bot


def clean_up(*args, dir_name="config"):
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


def download_all_photos(my_bot, media_id, filename: str, directory_name: str):
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


def get_all_photos(my_bot, nickname: str):
    twenty_last_medias = my_bot.get_total_user_medias(nickname)
    os.mkdir("photos" + "/" + nickname)
    for e, media_id in enumerate(twenty_last_medias):
        download_all_photos(my_bot, media_id, "img_" + str(e), nickname)


def get_photo_by_url(my_bot, url: str):
    # по url получаем id поста
    media_id = insta_bot.get_media_id_from_link(user_url)
    # по id поста получаем информацию о посте
    media = insta_bot.get_media_info(media_id)[0]
    # вытаскиваем из информации о посте ссылку на фото
    if "image_versions2" in media.keys():
        url = media["image_versions2"]["candidates"][0]["url"]
        # получаем фото
        response = requests.get(url)
        # сохраняем фото
        with open("photos" + "/" + "test.jpg", "wb") as f:
            response.raw.decode_content = True
            f.write(response.content)


target_name = "adim0k"


if __name__ == "__main__":
    clean_up()
    clean_up(target_name)
    insta_bot = connect()
    # get_all_photos(insta_bot, target_name)
    get_photo_by_url(insta_bot, user_url)
