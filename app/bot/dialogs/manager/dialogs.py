from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Group, Start
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory

from app.bot.dialogs.manager.getters import get_hello
from app.bot.states.admin.admin import AdminSG
from app.bot.states.manager.manager import ManagerSG
from .handlers import on_channel, on_create_post, on_settings


manager_dialog = Dialog(
    Window(
        Format("{hello_admin}"),
        Group(
            Button(
                text=Format("{create_post}"),
                id="create_post_pressed",
                on_click=on_create_post,
            ),
            Button(Format("{my_posts}"), id="edit_post_pressed"),
            # Button(Format("{create_description}"), id="create_descript_card_pressed"), # пока отложено
            Button(
                text=Format("{settings}"), id="settings_pressed", on_click=on_settings
            ),
            Button(
                text=Format("{add_channel}"),
                id="add_channel_pressed",
                on_click=on_channel,
            ),
            width=2,
        ),
        Start(
            Format("{to_admin_menu}"),
            id="to_admin_menu",
            state=AdminSG.start,
            when="is_admin",
        ),
        getter=get_hello,
        state=ManagerSG.start,
        markup_factory=ReplyKeyboardFactory(
            resize_keyboard=True,
            input_field_placeholder=Const("Выберите пункт меню"),
        ),
    )
)
