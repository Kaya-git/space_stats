from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


kb_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Сформировать очередь в паблики'),
        ]
    ],
    resize_keyboard=True
)

cancel_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Назад')
        ]
    ],
    resize_keyboard=True
)
