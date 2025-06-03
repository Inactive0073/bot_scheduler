from aiogram.fsm.state import State, StatesGroup


class ContentSG(StatesGroup):
    start = State()
    bot = State()
    today_info_bot = State()
    channel = State()
    today_info_channel = State()
    process_selected = State()