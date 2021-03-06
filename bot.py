import messages
import functions
import config
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import imagehash
from json_classes import ImagesHashes, PhotosData
from typing import Union
from PIL import Image
from keyboards.inline.likes_buttons import create_keyboard_with_8_buttons


token = config.BOT_TOKEN if not config.DEBUG else config.BOT_TOKEN_TEST
bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands="set_commands", state="*")
async def cmd_set_commands(message: types.Message):
    """Установить команды в боковой панели"""
    user_id = message.from_user.id
    if user_id == config.ADMIN_ID:
        commands = [types.BotCommand(command="/statistic", description="Статистика")]
        await bot.set_my_commands(commands)
        await message.answer("Команды установлены!")


@dp.message_handler(commands=["start"])
async def command_start(message: types.Message):
    """Начало работы, приветственное сообщение"""
    telegram_id = message.from_user.id
    if telegram_id == config.ADMIN_ID:
        await message.answer("Привет Босс!\n"
                             "Нажми /set_commands чтобы установить базовые команды")
    else:
        await message.answer(messages.promotion)


async def send_photos_group_to_chat(caption: str, count: int = config.POST_IN_ONE_TIME) -> None:
    """
    Отправить фотографии в телеграм канал
    Отбирает 8 рандомных фото (если их есть 8 и более)
    К первой фотографии добавляет коммент, который будет отображаться на всю группу фотографий
    Отправляет фотографии в телеграм канал и удаляет
    :param caption: Подпись под фотографиями
    :param count: Количество фотографий отправляемых единовременно (максимум 10)
    """
    images_len = functions.get_number_of_images()
    if images_len >= count:
        messages_ids = functions.get_n_random_message_id_from_data(count)
        photos = functions.get_photos(messages_ids, caption)
        chat_id = config.CHANNEL_RECIPIENT if not config.DEBUG else config.CHANNEL_RECIPIENT_TEST
        await bot.send_media_group(chat_id, photos)
        if not config.DEBUG:
            PhotosData.delete_images(messages_ids)
    else:
        await bot.send_message(config.ADMIN_ID, 'Фотки закончились!')


@dp.message_handler(content_types=['photo'])
async def scan_photo(message: types.Message):
    """
    Получить фотографию и добавить инфо о фото в базу
    message_id, photo_id, photo_hash
    {
    message_id: photo_id,
    message_id: photo_id,
    message_id: photo_id
    ...
    }
    """
    telegram_id = message.from_user.id
    chat_id = message.chat.id
    message_id = message.message_id
    photo_id = message.photo[-1].file_id
    if telegram_id == config.ADMIN_ID and message.chat.id in (config.CHANNEL_DONOR, config.ADMIN_ID):
        image_hash = await image_hash_in_base(photo_id)
        if image_hash:
            await bot.delete_message(chat_id, message_id)
        else:
            PhotosData.insert_new_data_in_json_file(message_id, photo_id)


async def get_photo_hash(photo_id: str):
    """Получить хэш фотографии"""
    photo = await bot.download_file_by_id(photo_id)
    photo_hash = imagehash.average_hash(Image.open(photo))
    return str(photo_hash)


async def image_hash_in_base(photo_id: str) -> Union[bool, None]:
    """
    Проверка хэш фотографии в базе хэшей
    Если есть - True, если нет - добавить хэш в базу и вернуть False
    :param photo_id: id фотографии в Телеграме
    :return: True или False
    """
    image_hash: str = await get_photo_hash(photo_id)
    all_hashes: list = ImagesHashes.get_data_from_json_file()
    if image_hash in all_hashes:
        return True
    else:
        ImagesHashes.insert_new_data_in_json_file(image_hash)


@dp.message_handler(commands=["statistic"])
async def command_statistic(message: types.Message):
    """Получить информацию о базе фотографий"""
    telegram_id = message.from_user.id
    if telegram_id == config.ADMIN_ID:
        images_len = functions.get_number_of_images()
        posts_day_count = round(images_len / config.POST_IN_DAY, 2)
        text = f"Всего: {images_len} фотографий\n" \
               f"Будет публиковаться: {posts_day_count} дней\n" \
               f"Время публикаций: {config.MORNING_POST_TIME} и {config.NIGHT_POST_TIME}"
        await message.answer(text)
    else:
        await message.answer(messages.promotion)


@dp.message_handler()
async def echo(message: types.Message):
    telegram_id = message.from_user.id
    if telegram_id == config.ADMIN_ID:
        await message.answer('...')
