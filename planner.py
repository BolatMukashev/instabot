import asyncio
import bot_config
import aioschedule
from bot import send_group_of_photos_to_chat, update_db


async def scheduler() -> None:
    """
    Асинхронный планировщик задач.
    Каждый день в указанное время отправляет фотографии в телеграм канал
    Каждый понедельник, среду и пятницу обновляет базу фотографий по сохраненным никнеймам
    """
    aioschedule.every().day.at(bot_config.MORNING_POST_TIME).do(send_group_of_photos_to_chat,
                                                                message='Утренняя подборка красавиц казашек\n'
                                                                        'Қазақ қыздарының сұлуларының таңғы таңдауы')
    aioschedule.every().day.at(bot_config.NIGHT_POST_TIME).do(send_group_of_photos_to_chat,
                                                              message='Вечерняя подборка красавиц казашек\n'
                                                                      'Қазақ қыздарының сұлуларының кешкі таңдауы')
    aioschedule.every().monday.at(bot_config.PHOTO_DB_UPDATE_TIME).do(update_db)
    aioschedule.every().wednesday.at(bot_config.PHOTO_DB_UPDATE_TIME).do(update_db)
    aioschedule.every().friday.at(bot_config.PHOTO_DB_UPDATE_TIME).do(update_db)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(30)


async def on_startup(_):
    asyncio.create_task(scheduler())