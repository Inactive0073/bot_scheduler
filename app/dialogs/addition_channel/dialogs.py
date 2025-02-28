from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Button, Url, SwitchTo

from app.dialogs.addition_channel.getters import get_main_info
from app.states.addition_channel import AdditionToChannelSG


dialog_addition_channel = Dialog(
    Window(
        Url(
            Format("{instruction_add_channel}"),
            url=Format("{url_button}"),
            id="add_channel_pressed"),
        state=AdditionToChannelSG.start,
    ),
    getter=get_main_info
)