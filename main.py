import functions

post_url = "https://www.instagram.com/p/CSpPlytISMS/?utm_source=ig_web_copy_link"
target_name = "adim0k"


if __name__ == "__main__":
    insta_bot = functions.connect()
    # functions.get_all_photos(insta_bot, target_name)
    functions.get_photo_by_url(insta_bot, post_url)
