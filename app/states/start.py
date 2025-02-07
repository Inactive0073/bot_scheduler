from aiogram.fsm.state import State, StatesGroup


class StartSG(StatesGroup):
    start = State()
    demo = State()  # Представление возможностей бота
