from aiogram.fsm.state import State, StatesGroup

class StartSG(StatesGroup):
    start = State()
    creating_post = State() # Создание поста
    demo = State() # Представление возможностей бота
    editing_text = State()
    add_url = State()
    set_time = State()
    set_notify = State()
    media = State()
    toggle_comments = State()
    push_now = State()