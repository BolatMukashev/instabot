from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import bot_config
import functions


bot = Bot(token=bot_config.BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
insta_bot = functions.connect()


@dp.message_handler(commands="set_commands", state="*")
async def cmd_set_commands(message: types.Message):
    """Установить команды в боковой панели"""
    user_id = message.from_user.id
    if user_id == bot_config.ADMIN_ID:
        commands = [types.BotCommand(command="/statistic", description="Статистика"),
                    types.BotCommand(command="/send_500_photo", description="Отправить 500 фото"),
                    types.BotCommand(command="/update_db", description="Обновить базу фотографий"),
                    types.BotCommand(command="/delete_all", description="Удалить все фото")]
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
        await message.answer("Несанкционированный доступ!")


@dp.message_handler(commands=["send_500_photo"])
async def command_send_500_photo(message: types.Message):
    """Отправить 500 фото в чат для 'затравки'"""
    telegram_id = message.from_user.id
    if telegram_id == bot_config.ADMIN_ID:
        await message.answer("Привет Босс!")
        images_len, posts_day_count = functions.get_len_images()
        if images_len > 500:
            for x in range(500):
                image_name = functions.random_choice_image()
                with open("photos/" + image_name, 'rb') as photo:
                    await bot.send_photo(bot_config.CHAT_ID, photo)
                    functions.delete_image(image_name)
    else:
        await message.answer("Несанкционированный доступ!")


@dp.message_handler(commands=["update_db"])
async def command_update_db(message: types.Message):
    """Пройдтись по базе никнеймов и добавить новые фотографии в директорию photos"""
    telegram_id = message.from_user.id
    if telegram_id == bot_config.ADMIN_ID:
        num = functions.update_all_users_photos(insta_bot)
        await message.answer(f"Привет Босс! Успешно добавлено {num} фотографии в базу")
    else:
        await message.answer("Несанкционированный доступ!")


@dp.message_handler(commands=["delete_all"])
async def command_delete_all(message: types.Message):
    """Удалить все фотографии из базы"""
    telegram_id = message.from_user.id
    if telegram_id == bot_config.ADMIN_ID:
        functions.delete_all_images()
        await message.answer("Привет Босс! Все фотографии в базе удалены")
    else:
        await message.answer("Несанкционированный доступ!")


@dp.message_handler(commands=["statistic"])
async def command_statistic(message: types.Message):
    """Получить информацию о базе фотографий"""
    telegram_id = message.from_user.id
    if telegram_id == bot_config.ADMIN_ID:
        images_len, posts_day_count = functions.get_len_images()
        text = f"Всего: {images_len} фотографий\n" \
               f"Будет публиковаться: {posts_day_count} дней"
        await message.answer(text)
    else:
        await message.answer("Несанкционированный доступ!")


@dp.message_handler()
async def echo(message: types.Message):
    telegram_id = message.from_user.id
    print(message.chat.id)
    if telegram_id == bot_config.ADMIN_ID:
        if message.text[:8] == "https://":
            post_url = message.text
            functions.download_photos_by_url(insta_bot, post_url)
            await message.answer("Фотографии из ссылки добавлены в базу")
        else:
            nickname = message.text
            functions.download_all_user_photos(insta_bot, nickname)
            if not bool(functions.check_data_in_json_file(bot_config.JSON_FILE_WITH_NICKNAMES, nickname)):
                functions.insert_new_data_in_json_file(bot_config.JSON_FILE_WITH_NICKNAMES, nickname)
            await message.answer("Фотографии пользователя добавлены в базу")
    else:
        await message.answer("Несанкционированный доступ!")
