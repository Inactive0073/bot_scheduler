from aiogram_dialog import Dialog, Window, ShowMode
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import (
    Group,
    SwitchTo,
    Toggle,
    Button,
    Multiselect,
    Calendar,
    Row,
    Start,
)
from aiogram_dialog.widgets.input import TextInput, MessageInput

from app.bot.states.manager import ManagerSG, ContentSG
from .getters import content_bot_data, content_channel_data, content_data
from .handlers import on_date_selected

content_dialog = Dialog(
    Window(
        Format("{content_hello_msg}"),
        Row(
            SwitchTo(Format("{content_bot_btn}"), id="bot_content", state=ContentSG.bot),
            SwitchTo(Format("{content_channel_btn}"), id="channel_content", state=ContentSG.channel),
        ),
        Start(Format("{main_menu}"), id="main_menu", state=ManagerSG.start),
        state=ContentSG.start
    ),
    # окно контента бота
    Window(
        Format("{bot_content_msg}"),
        Calendar(id="calendar", on_click=on_date_selected),
        state=ContentSG.bot,
        getter=content_bot_data    
    ),
    # окно контента канала
    Window(
        Format("{channel_content_msg}"),
        state=ContentSG.channel,
        getter=content_channel_data    
    ),
    getter=content_data
)