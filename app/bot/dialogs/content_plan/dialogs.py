from typing import Callable

from aiogram_dialog import Dialog, Window, ShowMode
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import (
    Group,
    SwitchTo,
    Toggle,
    Button,
    Back,
    Select,
    Calendar,
    Row,
    Start,
    ScrollingGroup
)
from aiogram_dialog.widgets.input import TextInput, MessageInput

from app.bot.states.manager import ManagerSG, ContentSG
from app.bot.utils.schemas.models import PostData
from .calendar_ import CustomCalendar
from .getters import content_bot_data, content_channel_data, content_data, content_today_bot_data
from .handlers import on_date_selected, on_post_selected, type_selected



post_id_getter: Callable[[PostData], str] = lambda item: item.schedule_id

content_dialog = Dialog(
    Window(
        Format("{content_hello_msg}"),
        Row(
            SwitchTo(
                Format("{content_bot_btn}"), 
                id="bot",
                state=ContentSG.bot,
                on_click=type_selected
            ),
            SwitchTo(
                Format("{content_channel_btn}"),
                id="channel",
                state=ContentSG.channel,
                on_click=type_selected
            ),
        ),
        Start(Format("{main_menu}"), id="main_menu", state=ManagerSG.start),
        state=ContentSG.start
    ),
    # окно контента бота
    Window(
        Format("{bot_content_msg}"),
        CustomCalendar(id="calendar", on_click=on_date_selected),
        SwitchTo(Format("{back}"), id="__back__", state=ContentSG.start),
        state=ContentSG.bot,
        getter=content_bot_data    
    ),
    # окно контента бота
    Window(
        Format("{today_info_msg}"),
        ScrollingGroup(
            Select(
                Format("{item.time} - {item.text}"),
                id="s_calendar",
                item_id_getter=post_id_getter,
                items="posts",
                on_click=on_post_selected
            ),
            id="sg_calendar",
            height=5,
            hide_on_single_page=True,
        ),
        SwitchTo(Format("{back}"), id="__back__", state=ContentSG.bot),
        getter=content_today_bot_data,
        state=ContentSG.today_info_bot
    ),
    # окно работы с постами на выбранный период
    Window(
        Format("{process_selected_post_msg}"),
        Button(Format("{to_cancel}"), id="delete_post", on_click=on_post_selected),
        Back(Format("{back}")),
        state=ContentSG.process_selected
    ),
    # окно контента канала
    Window(
        Format("{channel_content_msg}"),        
        Calendar(id="calendar", on_click=on_date_selected),
        SwitchTo(Format("{back}"), id="__back__", state=ContentSG.start),
        state=ContentSG.channel,
        getter=content_channel_data    
    ),
    
    getter=content_data
)