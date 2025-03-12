from aiogram_dialog import Dialog, LaunchMode, Window
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Url, SwitchTo

from app.dialogs.addition_channel.getters import get_url_info
from app.states.addition_channel import AdditionToChannelSG
from .handlers import check_admin_status


dialog_addition_channel = Dialog(
    Window(
        Format("{instruction_add_channel}"),
        Url(
            text=Const("Добавить канал"),
            url=Format("{url_button}"),
            id="add_channel_pressed",
        ),
        state=AdditionToChannelSG.start,
        getter=get_url_info,
        on_process_result=check_admin_status,
    ),
    launch_mode=LaunchMode.EXCLUSIVE
)
