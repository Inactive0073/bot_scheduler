from aiogram_dialog import Dialog, LaunchMode, Window
from aiogram_dialog.widgets.text import Format, Const, Case
from aiogram_dialog.widgets.kbd import Button, Url, SwitchTo, Group
from aiogram_dialog.widgets.input import TextInput

from app.states.addition_channel import AdditionToChannelSG
from .getters import get_url_info
from .handlers import check_admin_status, validate_channel


dialog_addition_channel = Dialog(
    Window(
        Case(
            {
                1:Format("{channel_exists_message}"),
                0:Format("{channel_not_exists_message}"),
            },
            selector="channel_exists",
            ),
        Format("{instruction_add_channel}"),
        Group(
            
        ),
        Url(
            text=Format("{url_button_name}"),
            url=Format("{url_button}"),
            id="add_channel_pressed",
        ),
        TextInput(
            id="chhanel_check_bot_status",
            type_factory=validate_channel,
            on_success=check_admin_status,
        ),
        state=AdditionToChannelSG.start,
        getter=get_url_info,
    )
)
