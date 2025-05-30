from aiogram.fsm.state import State, StatesGroup


class ContentSG(StatesGroup):
    start = State()
    bot = State()
    channel = State()