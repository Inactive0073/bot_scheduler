from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window, ShowMode
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Group, SwitchTo, Back, Toggle, Button
from aiogram_dialog.widgets.input import TextInput, MessageInput

from app.dialogs.creating_post.getters import (
    get_creating_post_data,
    get_watch_text,
    get_url_instruction,
)
from app.dialogs.creating_post.handlers import (
    process_delete_button,
    process_other_type_msg,
    process_post_msg,
    process_button_case,
    process_invalid_button_case,
    edit_text,
)
from app.dialogs.creating_post.services import parse_button

from app.states.creating_post import PostingSG

create_post_dialog = Dialog(
    # Процесс создания поста
    Window(
        # Записываем текст введенный пользователем
        Format("{watch_text}"),
        MessageInput(
            func=process_post_msg, content_types=[ContentType.PHOTO, ContentType.TEXT]
        ),
        MessageInput(
            func=process_other_type_msg,
        ),
        state=PostingSG.watch_text,
        getter=get_watch_text,
    ),
    Window(
        # =============================================================
        # Меню настройки поста
        # =============================================================
        # Редактировать пост | Добавить URL кнопок / Удалить URL кнопки
        # Время отправки     | С уведомлением / Без уведомления
        # Добавить медиа     | Отключить комментарии
        # Отправить сейчас
        # =============================================================
        Format("{reply_title}\n"),
        Group(
            # Отредактировать текст поста
            SwitchTo(
                Format("{edit}"),
                id="edit_text_pressed",
                state=PostingSG.editing_text,
                show_mode=ShowMode.DELETE_AND_SEND,
            ),
            # Добавить URL кнопок
            SwitchTo(
                Format("{url}"),
                id="add_url_pressed",
                state=PostingSG.add_url,
                when="url_button_empty",
                show_mode=ShowMode.DELETE_AND_SEND,
            ),
            # Удалить URL кнопок
            Button(
                Format("{url_delete}"),
                id="del_url_pressed",
                on_click=process_delete_button,
                when="url_button_exists",
            ),
            # Установить время
            SwitchTo(
                Format("{set_time}"), id="set_time_pressed", state=PostingSG.set_time
            ),
            SwitchTo(
                Format("{set_notify}"),
                id="set_notify_pressed",
                state=PostingSG.set_notify,
            ),
            SwitchTo(Format("{media}"), id="media_pressed", state=PostingSG.media),
            SwitchTo(
                Format("{unset_comments}"),
                id="unset_comments_pressed",
                state=PostingSG.toggle_comments,
            ),
            SwitchTo(
                Format("{push_now}"), id="push_now_pressed", state=PostingSG.push_now
            ),
            width=2,
        ),
        state=PostingSG.creating_post,
        getter=get_creating_post_data,
    ),
    # окно редактирования текста поста
    Window(
        Format("{watch_text}"),
        TextInput(
            id="watch_edit_text",
            on_success=edit_text,
        ),
        state=PostingSG.editing_text,
        getter=get_watch_text,
    ),
    # окно добавления кнопок к сообщению
    Window(
        Format("{instruction_url}"),
        TextInput(
            id="watch_url_button",
            on_success=process_button_case,
            on_error=process_invalid_button_case,
            type_factory=parse_button,
        ),
        MessageInput(func=process_other_type_msg, content_types=ContentType.ANY),
        state=PostingSG.add_url,
        getter=get_url_instruction,
    ),
    # окно добавления времени постинга 
    Window(
        Format("{instruction_delayed_post}"),
        
    ),
)
