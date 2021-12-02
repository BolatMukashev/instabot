import asyncio
import messages
import config
import aioschedule
# from bot import send_photos_group_to_chat
#
#
# async def scheduler() -> None:
#     """
#     Асинхронный планировщик задач.
#     Каждый день в указанное время отправляет фотографии в телеграм канал
#     """
#     aioschedule.every().day.at(bot_config.MORNING_POST_TIME).do(send_photos_group_to_chat,
#                                                                 message=messages.photo_album_morning_caption)
#     aioschedule.every().day.at(bot_config.NIGHT_POST_TIME).do(send_photos_group_to_chat,
#                                                               message=messages.photo_album_night_caption)
#     while True:
#         await aioschedule.run_pending()
#         await asyncio.sleep(30)
#
#
# async def on_startup(_):
#     asyncio.create_task(scheduler())
