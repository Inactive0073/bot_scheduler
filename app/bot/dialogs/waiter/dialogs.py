from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import (
    WebApp,
)

from .getters import get_common_data

waiter_dialog = Dialog(
    Window(
        Format("{hello_waiter}"),
        WebApp(Format("{waiter_menu_scan}"), url=Format("{waiter_menu_scan_url}")),
    ),
    getter=get_common_data,
)
