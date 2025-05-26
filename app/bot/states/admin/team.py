from aiogram.fsm.state import State, StatesGroup


class TeamSG(StatesGroup):
    invite = State()
    kick = State()
