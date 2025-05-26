from aiogram.fsm.state import State, StatesGroup


class ReportsSG(StatesGroup):
    users = State()
    posts = State()
    bonuses = State()
