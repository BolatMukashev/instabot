from aiogram import executor
from functions import create_base_directory
from planner import on_startup


if __name__ == "__main__":
    create_base_directory()
    from bot import dp
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
