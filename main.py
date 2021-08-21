import functions

post_url = "https://www.instagram.com/p/CSpPlytISMS/?utm_source=ig_web_copy_link"
target_name = "adim0k"


if __name__ == "__main__":
    insta_bot = functions.connect()
    # functions.download_all_user_photos(insta_bot, target_name)
    functions.download_photos_by_url(insta_bot, post_url)
