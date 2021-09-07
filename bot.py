import time
import messages
import functions
import bot_config
from json_classes import Nicknames
from tqdm import tqdm as loading_bar
from aiogram.types import InputMediaPhoto
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(token=bot_config.BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
# insta_bot = functions.connect()


images_folder = bot_config.PHOTO_SAVE_FOLDER_NAME + '/'


@dp.message_handler(commands="set_commands", state="*")
async def cmd_set_commands(message: types.Message):
    """Установить команды в боковой панели"""
    user_id = message.from_user.id
    if user_id == bot_config.ADMIN_ID:
        commands = [types.BotCommand(command="/statistic", description="Статистика"),
                    types.BotCommand(command="/send_100_photo", description="Отправить 100 фото")]
        await bot.set_my_commands(commands)
        await message.answer("Команды установлены!")


@dp.message_handler(commands=["start"])
async def command_start(message: types.Message):
    """Начало работы, приветственное сообщение"""
    telegram_id = message.from_user.id
    if telegram_id == bot_config.ADMIN_ID:
        await message.answer("Привет Босс!\n"
                             "Нажми /set_commands чтобы установить базовые команды")
    else:
        await message.answer(messages.promotion)


@dp.message_handler(commands=["send_100_photo"])
async def command_send_100_photo(message: types.Message):
    """Отправить 100 фото в чат для 'затравки'"""
    telegram_id = message.from_user.id
    if telegram_id == bot_config.ADMIN_ID:
        images_len, posts_day_count = functions.get_number_of_images()
        if images_len > 100:
            for x in range(10):
                images_names = functions.get_random_images_names(bot_config.POST_IN_ONE_TIME)
                functions.paste_watermarks_to_images(images_names)
                message = "Порцию сексуальных казашек заказывали?\n" \
                          "Сексуалды қазақ қыздарына тапсырыс бердіңіз бе?\n" \
                          "#казашки #қазақ #қыздар"
                media = [InputMediaPhoto(open(images_folder + images_names[0], 'rb'), message)]
                for photo_name in images_names[1:bot_config.POST_IN_ONE_TIME]:
                    media.append(InputMediaPhoto(open(images_folder + photo_name, 'rb')))
                await bot.send_media_group(bot_config.CHANNEL_NAME, media)
                functions.delete_images(images_names)
                time.sleep(60)
            await bot.send_message(bot_config.ADMIN_ID, 'Все 100 фотографии опубликованы')
    else:
        await message.answer(messages.promotion)


async def send_group_of_photos_to_chat(message: str, count: int = bot_config.POST_IN_ONE_TIME) -> None:
    """
    Отправить фотографии в телеграм канал.
    Отбирает 10 рандомных фото (если их есть 10 и более).
    К первой фотографии добавляет коммент, который будет отображаться на всю группу фотографий.
    Отправляет фотографии в телеграм канал и удаляет.
    :param message: Подпись под фотографиями
    :param count: Количество фотографий отправляемых единовременно (максимум 10)
    """
    images_len, _ = functions.get_number_of_images()
    if images_len >= count:
        images_names = functions.get_random_images_names(count)
        functions.paste_watermarks_to_images(images_names)
        media = [InputMediaPhoto(open(images_folder + images_names[0], 'rb'), message)]
        for photo_name in loading_bar(images_names[1:count], desc='Объединение фотографий в группу'):
            media.append(InputMediaPhoto(open(images_folder + photo_name, 'rb')))
        await bot.send_media_group(bot_config.CHANNEL_NAME, media)
        functions.delete_images(images_names)


async def update_db():
    """Пройдтись по базе никнеймов и добавить новые фотографии в директорию photos"""
    num = functions.update_all_users_photos(insta_bot)
    await bot.send_message(chat_id=bot_config.ADMIN_ID,
                           text=f"Привет Босс! Успешно добавлено {num} фотографии в базу")


@dp.message_handler(commands=["delete_all"])
async def command_delete_all(message: types.Message):
    """Удалить все фотографии из базы"""
    telegram_id = message.from_user.id
    if telegram_id == bot_config.ADMIN_ID:
        functions.delete_all_images()
        await message.answer("Привет Босс! Все фотографии в базе удалены")
    else:
        await message.answer(messages.promotion)


@dp.message_handler(commands=["statistic"])
async def command_statistic(message: types.Message):
    """Получить информацию о базе фотографий"""
    telegram_id = message.from_user.id
    if telegram_id == bot_config.ADMIN_ID:
        images_len, posts_day_count = functions.get_number_of_images()
        text = f"Всего: {images_len} фотографий\n" \
               f"Будет публиковаться: {posts_day_count} дней"
        await message.answer(text)
    else:
        await message.answer(messages.promotion)


@dp.message_handler()
async def echo(message: types.Message):
    telegram_id = message.from_user.id
    if telegram_id == bot_config.ADMIN_ID:
        if message.text[:8] == "https://":
            post_url, media_numbers = functions.get_post_url_and_media_numbers(message.text)
            image_name = functions.download_photos_by_url(insta_bot, post_url, media_numbers)
            await message.answer(f"Фотографии из ссылки добавлены в базу под именем\n"
                                 f"{image_name}")
        else:
            nickname, start, stop = functions.get_nickname_and_download_limits(message.text)
            if not bool(Nicknames.check_data_in_json_file(nickname)):
                Nicknames.insert_new_data_in_json_file(nickname)
            functions.download_all_user_photos(insta_bot, nickname, start, stop)
            await message.answer("Фотографии пользователя добавлены в базу")
    else:
        await message.answer(messages.promotion)
