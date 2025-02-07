from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Group, Start
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory

from app.dialogs.start.getters import get_hello
from app.states.start import StartSG
from app.states.creating_post import PostingSG


start_dialog = Dialog(
    Window(
        Format("{hello_admin}"),
        Group(
            Start(
                Format("{create_post}"),
                id="create_post_pressed",
                state=PostingSG.watch_text,
            ),
            Button(Format("{edit_post}"), id="edit_post_pressed"),
            # Button(Format("{create_description}"), id="create_descript_card_pressed"), # пока отложено
            Button(Format("{settings}"), id="settings_pressed"),
            width=2,
        ),
        getter=get_hello,
        state=StartSG.start,
        markup_factory=ReplyKeyboardFactory(
            resize_keyboard=True, input_field_placeholder=Const("Выберите пункт меню")
        ),
    )
)
