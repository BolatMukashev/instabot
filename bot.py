from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config
import functions


bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
insta_bot = functions.connect()


@dp.message_handler(commands="set_commands", state="*")
async def cmd_set_commands(message: types.Message):
    """Установить команды в боковой панели"""
    user_id = message.from_user.id
    if user_id == config.ADMIN_ID:
        commands = [types.BotCommand(command="/delete_all", description="Удалить все фото"),
                    types.BotCommand(command="/statistic", description="Статистика")]
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
        await message.answer("Несанкционированный доступ!")


@dp.message_handler(commands=["delete_all"])
async def command_delete_all(message: types.Message):
    """Удалить все фотографии из базы"""
    telegram_id = message.from_user.id
    if telegram_id == config.ADMIN_ID:
        functions.delete_all_images()
        await message.answer("Привет Босс! Все фотографии в базе удалены")
    else:
        await message.answer("Несанкционированный доступ!")


@dp.message_handler(commands=["statistic"])
async def command_statistic(message: types.Message):
    """Получить информацию о базе фотографий"""
    telegram_id = message.from_user.id
    if telegram_id == config.ADMIN_ID:
        text = functions.get_len_images()
        await message.answer(text)
    else:
        await message.answer("Несанкционированный доступ!")


@dp.message_handler()
async def echo(message: types.Message):
    telegram_id = message.from_user.id
    print(message.chat.id)
    if telegram_id == config.ADMIN_ID:
        if message.text[:8] == "https://":
            post_url = message.text
            functions.download_photos_by_url(insta_bot, post_url)
            await message.answer("Фотографии из ссылки добавлены в базу")
            # image_name = functions.random_choice_image()
            # with open("photos/" + image_name, 'rb') as photo:
            #     await bot.send_photo(config.CHAT_ID, photo)
        else:
            nickname = message.text
            functions.download_all_user_photos(insta_bot, nickname)
            await message.answer("Фотографии пользователя добавлены в базу")
    else:
        await message.answer("Несанкционированный доступ!")




