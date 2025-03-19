from aiogram.fsm.state import State, StatesGroup


class AdditionToChannelSG(StatesGroup):
    start = State()
    channel_settings = State()
    delete_bot_from_channel = State()
