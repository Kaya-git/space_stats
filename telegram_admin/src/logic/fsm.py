from aiogram.fsm.state import StatesGroup, State


class TgTasksStates(StatesGroup):
    tg_group = State()
    product_links = State()
