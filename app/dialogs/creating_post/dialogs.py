from aiogram import F
from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window, ShowMode
from aiogram_dialog.widgets.text import Format, Case, List
from aiogram_dialog.widgets.kbd import (
    Group,
    SwitchTo,
    Toggle,
    Button,
    Multiselect,
    Row,
    Start,
)
from aiogram_dialog.widgets.input import TextInput, MessageInput

from .getters import (
    get_addition_media_data,
    get_approve_push_data,
    get_creating_post_data,
    get_preselect_channel_data,
    get_push_later_data,
    get_report_after_push_data,
    get_time_instruction_data,
    get_watch_text,
    get_url_instruction,
    get_posting_sg_common_data,
)
from .handlers import (
    invalid_set_time,
    process_delete_button,
    process_other_type_msg,
    process_post_msg,
    process_addition_media,
    process_button_case,
    process_invalid_button_case,
    process_invalid_media_content,
    edit_text,
    process_push_to_bot_button,
    process_push_now_to_channel_button,
    process_remove_media,
    process_send_to_channel_later,
    process_set_time,
    process_to_select_bot_mailing,
    process_to_select_channel,
    process_toggle_notify,
)
from .services import parse_button, parse_time

from app.states.creating_post import PostingSG
from app.states.start import StartSG

create_post_dialog = Dialog(
    # Процесс создания поста
    # окно выбора каналов для публикаций
    Window(
        Format("{select_channel_message}"),
        SwitchTo(
            Format("{mail_to_bots_subscribers_message}"),
            id="bot_sending_selected",
            state=PostingSG.watch_text,
            on_click=process_to_select_bot_mailing,
        ),
        Multiselect(
            checked_text=Format("✅ {item[1]}"),
            unchecked_text=Format("{item[1]}"),
            id="selected_channel_for_publication",
            item_id_getter=lambda item: item[2],
            items="all_channels",
            on_click=process_to_select_channel,
        ),
        Row(
            Start(Format("{back}"), id="back_to_menu", state=StartSG.start),
            SwitchTo(
                Format("{next}"),
                id="next_clicked",
                state=PostingSG.watch_text,
                when=F["one_or_more_selected"],
            ),
        ),
        getter=get_preselect_channel_data,
        state=PostingSG.select_channels,
    ),
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
        # Время отправки / Редактировать время     | С уведомлением / Без уведомления
        # Добавить медиа / Удалить медиа     | Отключить комментарии
        # Отправить сейчас
        # Назад
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
            Group(
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
            ),
            # Установить время
            SwitchTo(
                Case(
                    texts={
                        0: Format("{set_time}"),
                        1: Format("{posting_time}"),
                    },
                    selector="posting_time_index",
                ),
                id="set_time_pressed",
                state=PostingSG.set_time,
                show_mode=ShowMode.DELETE_AND_SEND,
            ),
            # Уведомление
            Toggle(
                Format("{item.desc}"),
                id="set_notify_pressed",
                items="states_notify",
                item_id_getter=lambda notify: notify.id,
                on_click=process_toggle_notify,
            ),
            # Медиа
            Group(
                SwitchTo(
                    Format("{media_message}"), id="media_pressed", state=PostingSG.media
                ),
                Button(
                    Format("{delete_media_message}"),
                    id="delete_media_pressed",
                    on_click=process_remove_media,
                    when=F["has_media"],
                ),
            ),
            # Включение/отключение комментариев
            SwitchTo(
                Format("{unset_comments}"),
                id="unset_comments_pressed",
                state=PostingSG.toggle_comments,
            ),
            # Отправить сейчас
            SwitchTo(
                Format("{push_now}"), id="push_now_pressed", state=PostingSG.push_now
            ),
            # Запланировать пост
            SwitchTo(
                Format("{push_later}"),
                id="push_later_pressed",
                state=PostingSG.push_later,
                when=F["posting_time"],
            ),
            width=2,
        ),
        SwitchTo(Format("{back}"), id="__back__", state=PostingSG.select_channels),
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
        TextInput(
            id="time_set",
            type_factory=parse_time,
            on_success=process_set_time,
            on_error=invalid_set_time,
        ),
        state=PostingSG.set_time,
        getter=get_time_instruction_data,
    ),
    # окно добавления медиа
    Window(
        Format("{instruction_add_media}"),
        MessageInput(
            func=process_addition_media,
            content_types=[ContentType.PHOTO, ContentType.VIDEO],
        ),
        MessageInput(func=process_invalid_media_content),
        state=PostingSG.media,
        getter=get_addition_media_data,
    ),
    # окно моментальной отправки
    Window(
        Format("{push_now_approve_message}"),
        Group(
            SwitchTo(
                Format("{cancel_caption}"), id="__back__", state=PostingSG.creating_post
            ),
            Button(
                Format("{yes_caption}"),
                id="push_now_pressed",
                on_click=process_push_now_to_channel_button,
                when=F["dialog_data"]["recipient_type"] != "bot",
            ),
            Button(
                Format("{yes_caption}"),
                id="push_now_bot_pressed",
                on_click=process_push_to_bot_button,
                when=F["dialog_data"]["recipient_type"] == "bot",
            ),
            width=2,
        ),
        state=PostingSG.push_now,
        getter=get_approve_push_data,
    ),
    # Окно отображения статуса отправленного поста
    Window(
        Format("{report_message}"),
        List(Format("└ {item[1]}"), items="channels"),
        Format("\n\n{autocaption}"),
        state=PostingSG.show_posted_status,
        getter=get_report_after_push_data,
    ),
    # Окно планирования поста
    Window(
        Format("{schedule_message}"),
        List(Format("└ {item[1]}"), items="selected_channels"),
        Group(
            SwitchTo(Format("{back}"), id="__back__", state=PostingSG.creating_post),
            Button(
                Format("{schedule_button_caption}"),
                id="push_later_channel_pressed",
                on_click=process_send_to_channel_later,
                when=F["dialog_data"]["recipient_type"] != "bot",
            ),
            Button(
                Format("{schedule_button_caption}"),
                id="push_later_bot_pressed",
                on_click=process_push_to_bot_button,
                when=F["dialog_data"]["recipient_type"] == "bot",
            ),
            width=2,
        ),
        state=PostingSG.push_later,
        getter=get_push_later_data,
    ),
    getter=get_posting_sg_common_data,
)
