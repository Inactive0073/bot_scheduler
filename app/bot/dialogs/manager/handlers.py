from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button

from app.bot.states.manager.addition_channel import AdditionToChannelSG
from app.bot.states.manager.creating_post import PostingSG
from app.bot.states.manager.settings import SettingsSG


async def on_create_post(
    message: Message, button: Button, dialog_manager: DialogManager
) -> None:
    is_admin = dialog_manager.start_data.get("is_admin")
    await dialog_manager.start(
        state=PostingSG.select_channels,
        data={"is_admin": is_admin},
        show_mode=ShowMode.DELETE_AND_SEND,
    )


async def on_settings(
    message: Message, button: Button, dialog_manager: DialogManager
) -> None:
    is_admin = dialog_manager.start_data.get("is_admin")
    await dialog_manager.start(
        state=SettingsSG.start,
        data={"is_admin": is_admin},
        show_mode=ShowMode.DELETE_AND_SEND,
        )


async def on_channel(
    message: Message, button: Button, dialog_manager: DialogManager
) -> None:
    is_admin = dialog_manager.start_data.get("is_admin")
    await dialog_manager.start(
        state=AdditionToChannelSG.start, 
        data={"is_admin": is_admin},
        show_mode=ShowMode.DELETE_AND_SEND,
    )
