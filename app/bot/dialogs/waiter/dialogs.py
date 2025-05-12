from aiogram import F
from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window, ShowMode
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import (
    Group,
    SwitchTo,
    Button,
    Multiselect,
    Row,
    Start,
    WebApp,
)
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory

from .getters import get_common_data

waiter_dialog = Dialog(
    Window(
        Format("{hello_waiter}"),
        WebApp(Format("{waiter_menu_scan}"), url=Format("{waiter_menu_scan_url}")),
    ),
    getter=get_common_data,
)
