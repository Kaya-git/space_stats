from aiogram import Router, types, F
from aiogram.types import CallbackQuery, Message
from asyncio import sleep
from keyboards.inline import get_inline_keyboard
from aiogram.fsm.context import FSMContext
from fsm import TgTasksStates
from config import conf
from keyboards.reply import cancel_button, kb_main_menu
from handlers import form_links_list


set_tg_tasks = Router(name="set_telegram_task")


@set_tg_tasks.message(F.text == "Сформировать очередь в паблики")
async def select_tg_channel(message: types.Message):
    await message.answer(
        text="Выбери тг канал",
        reply_markup=get_inline_keyboard()
    )


@set_tg_tasks.callback_query()
async def select_part_number(call: CallbackQuery, state:  FSMContext) -> None:
    await state.set_state(TgTasksStates.tg_group)
    await state.update_data(tg_group=call.data)
    await state.set_state(TgTasksStates.product_links)
    await call.message.answer(
        text='А теперь оставь ссылки с товарами через пробел',
        reply_markup=cancel_button
    )


@set_tg_tasks.message(TgTasksStates.product_links)
async def load_product_link(message: Message, state: FSMContext) -> None:
    await state.update_data(product_links=message.text)
    user_data = state.get_data()
    links_list = await form_links_list(user_data["product_links"])
    """ Отправляем в rbtmq на парсер"""

    await message.reply(
        "Задание отправленно в брокер для дальнейщей передачи парсеру",
        reply_markup=kb_main_menu
    )
    await state.clear()
