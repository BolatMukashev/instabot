import os
import shutil
import requests
from instabot import Bot
from config import INST_USERNAME, INST_PASSWORD


user_url = "https://www.instagram.com/p/CSGTtd9qfyU/?utm_medium=copy_link"


def connect():
    bot = Bot()
    bot.login(username=INST_USERNAME, password=INST_PASSWORD)
    return bot


def clean_up(dir_name="config"):
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
        with open(directory_name + "/" + filename + ".jpg", "wb") as f:
            response.raw.decode_content = True
            f.write(response.content)
    elif "carousel_media" in media.keys():
        for e, element in enumerate(media["carousel_media"]):
            url = element['image_versions2']["candidates"][0]["url"]
            response = requests.get(url)
            with open(directory_name + "/" + filename + str(e) + ".jpg", "wb") as f:
                response.raw.decode_content = True
                f.write(response.content)


def get_all_photos(my_bot, nickname: str):
    twenty_last_medias = my_bot.get_total_user_medias(nickname)
    os.mkdir(nickname)
    for e, media_id in enumerate(twenty_last_medias):
        download_all_photos(my_bot, media_id, "img_" + str(e), nickname)


if __name__ == "__main__":
    clean_up()
    clean_up("mesu.mesu")
    insta_bot = connect()
    get_all_photos(insta_bot, "mesu.mesu")

