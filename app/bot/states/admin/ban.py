from aiogram.fsm.state import State, StatesGroup

class BanSG(StatesGroup):
    ban = State()
    unban = State()