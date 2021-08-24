from aiogram import executor
from functions import create_base_directory
import asyncio
import aioschedule
from bot import send_photo_to_chat


async def scheduler() -> None:
    """
    Асинхронный планировщик задач. Каждый день в указанное время отправляет фотографии в телеграм канал
    """
    aioschedule.every().day.at('8:30').do(send_photo_to_chat, message='Утренняя подборка красавиц')
    aioschedule.every().day.at('6:30').do(send_photo_to_chat, message='Вечерняя подборка секси казашек')
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())


if __name__ == "__main__":
    create_base_directory()
    from bot import dp
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
