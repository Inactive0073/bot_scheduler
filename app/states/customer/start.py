from aiogram.fsm.state import State, StatesGroup


class StartCustomerSG(StatesGroup):
    start = State()
    name = State()
    surname = State()
    email = State()
    birthday = State()
    gender = State()
    thanks = State()
