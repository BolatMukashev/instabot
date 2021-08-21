import functions

user_url = "https://www.instagram.com/p/CSwTRIDoJlm/?utm_source=ig_web_copy_linkk"
target_name = "adim0k"


if __name__ == "__main__":
    functions.clean_up()
    functions.clean_up(target_name)
    insta_bot = functions.connect()
    # functions.get_all_photos(insta_bot, target_name)
    functions.get_photo_by_url(insta_bot, user_url)
