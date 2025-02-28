from aiogram.fsm.state import State, StatesGroup


class AdditionToChannelSG(StatesGroup):
    start = State()