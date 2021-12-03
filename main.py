from aiogram import executor
from planner import on_startup


if __name__ == "__main__":
    from bot import dp
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
