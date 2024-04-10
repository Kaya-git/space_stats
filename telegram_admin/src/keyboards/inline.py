from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import tg_channels_controll


def pick_tg_channel_inline_keyboard():
    inline_keyboard_builder = InlineKeyboardBuilder()
    for channel_name in tg_channels_controll:
        inline_keyboard_builder.button(
            text=channel_name,
            callback_data=channel_name
        )
    return inline_keyboard_builder.as_markup()


def get_start_inline_keyboard():
    inline_keyboard_builder = InlineKeyboardBuilder()
    inline_keyboard_builder.button(
        text='156194946',
        callback_data='156194946'
    )
    inline_keyboard_builder.button(
        text='Назначить задачи на канал',
        callback_data='set_tg_tasks'
    )
    return inline_keyboard_builder.as_markup()
