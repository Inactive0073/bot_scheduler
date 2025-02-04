from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format, Const, Case
from aiogram_dialog.widgets.kbd import Button, Group, SwitchTo, Start
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory

from dialogs.start.getters import (
    get_hello, get_creating_post_data,
    get_watch_text, 
)
from dialogs.start.handlers import (
    process_post_msg,
    process_other_type_msg
)
from states.start import StartSG, PostingSG


start_dialog = Dialog(
    Window(
        Format('{hello_admin}'),
        Group(
            Start(
                Format('{create_post}'),
                id='create_post_pressed',
                state=PostingSG.watch_text,
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
            input_field_placeholder=Const('Выберите пункт меню')
        )
    )
)
create_post_dialog = Dialog(
    Window(
        Format('{watch_text}'),
        MessageInput(
            func=process_post_msg,
            content_types=[ContentType.PHOTO, ContentType.TEXT]
        ),
        MessageInput(
            func=process_other_type_msg,
        ),
        state=PostingSG.watch_text,
        getter=get_watch_text
    ),
    Window(
        Format('{reply_title}\n{post_message}'),
        Group(
            SwitchTo(
                Format('{edit}'),
                id='edit_text_pressed',
                state=PostingSG.editing_text,
            ),
            SwitchTo(
                Format('{url}'),
                id='add_url_pressed',
                state=PostingSG.add_url
            ),
            SwitchTo(
                Format('{set_time}'),
                id='set_time_pressed',
                state=PostingSG.set_time
            ),
            SwitchTo(
                Format('{set_notify}'),
                id='set_notify_pressed',
                state=PostingSG.set_notify
            ),
            SwitchTo(
                Format('{media}'),
                id='media_pressed',
                state=PostingSG.media
            ),
            SwitchTo(
                Format('{unset_comments}'),
                id='unset_comments_pressed',
                state=PostingSG.toggle_comments
            ),
            SwitchTo(
                Format('{push_now}'),
                id='push_now_pressed',
                state=PostingSG.push_now
            ),
            width=2
        ),
        state=PostingSG.creating_post,
        getter=get_creating_post_data,
    )
)
