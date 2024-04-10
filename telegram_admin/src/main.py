from aiogram import Bot, Dispatcher, types
from config import conf
from aiogram.filters import CommandStart
from keyboards.reply import kb_main_menu


bot = Bot(token=conf.telegram.bot_token)
dp = Dispatcher()


@dp.message(CommandStart())
async def handle_start(message: types.Message):
    await message.answer(
        text="""Привет, выбери задание""",
        reply_markup=kb_main_menu()
    )
    await message.delete()
