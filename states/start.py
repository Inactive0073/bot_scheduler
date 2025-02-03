from aiogram.fsm.state import State, StatesGroup

class StartSG(StatesGroup):
    start = State()
    demo = State() # Представление возможностей бота
    

class PostingSG(StatesGroup):
    watch_text = State()
    creating_post = State() # Создание поста
    editing_text = State()
    add_url = State()
    set_time = State()
    set_notify = State()
    media = State()
    toggle_comments = State()
    push_now = State()