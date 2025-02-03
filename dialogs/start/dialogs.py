from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Group, SwitchTo
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory

from dialogs.start.getters import get_hello, get_creating_post_data
from dialogs.start.handlers import create_post_click
from states.start import StartSG

start_dialog = Dialog(
    Window(
        Format('{hello_admin}'),
        Group(
            SwitchTo(
                Format('{create_post}'),
                id='create_post_pressed',
                state=StartSG.creating_post,
                on_click=create_post_click
            ),
            Button(
                Format('{edit_post}'),
                id='edit_post_pressed'
            ),
            Button(
                Format('{create_description}'),
                id='create_descript_card_pressed'
            ),
            Button(
                Format('{settings}'),
                id='settings_pressed'
            ),
            width=2,
        ),
        getter=get_hello,
        state=StartSG.start,
        markup_factory=ReplyKeyboardFactory(
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder=Const('Выберите пункт меню')
        )
    ),
    Window(
        Format('{reply_title}\n{msg_to_reply}'),
        Group(
            SwitchTo(
                Format('{edit}'),
                id='edit_text_pressed',
                state=StartSG.editing_text,
            ),
            SwitchTo(
                Format('{url}'),
                id='add_url_pressed',
                state=StartSG.add_url
            ),
            SwitchTo(
                Format('{set_time}'),
                id='set_time_pressed',
                state=StartSG.set_time
            ),
            SwitchTo(
                Format('{set_notify}'),
                id='set_notify_pressed',
                state=StartSG.set_notify
            ),
            SwitchTo(
                Format('{media}'),
                id='media_pressed',
                state=StartSG.media
            ),
            SwitchTo(
                Format('{unset_comments}'),
                id='unset_comments_pressed',
                state=StartSG.toggle_comments
            ),
            SwitchTo(
                Format('{push_now}'),
                id='push_now_pressed',
                state=StartSG.push_now
            ),
            width=2
        ),
        state=StartSG.creating_post,
        getter=get_creating_post_data
    ),
)