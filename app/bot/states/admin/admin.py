from aiogram.fsm.state import State, StatesGroup


class AdminSG(StatesGroup):
    start = State()
    reports = State()
    ban_menu = State()
    team = State()
