from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_keyboard_with_8_buttons():
    """Создать клавиатуру из 8 элементов"""
    keyboard = InlineKeyboardMarkup(row_width=4)
    for el in range(1, 9):
        button = InlineKeyboardButton(text=str(el), url='https://google.com')
        keyboard.insert(button)
    return keyboard
