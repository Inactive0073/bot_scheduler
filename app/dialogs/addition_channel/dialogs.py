from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format, Case
from aiogram_dialog.widgets.kbd import Button, Url, SwitchTo, Select, Group, Back
from aiogram_dialog.widgets.input import TextInput

from app.states.addition_channel import AdditionToChannelSG
from .getters import get_channel_settings, get_data_for_delete, get_url_info
from .handlers import (
    add_caption_to_channel,
    check_admin_status,
    delete_channel_from_bot,
    on_channel_selected,
    validate_channel,
)


dialog_addition_channel = Dialog(
    Window(
        Case(
            {
                1: Format("{channel_exists_message}"),
                0: Format("{channel_not_exists_message}"),
            },
            selector="channel_exists",
        ),
        Format("{instruction_add_channel}"),
        Group(
            Select(
                Format("{item[1]}"),  # Структура item:
                # [channel_id, channel_name,channel_username,channel_link,admin_id,]
                id="selected_channel",
                item_id_getter=lambda x: x[0],
                items="channels",
                on_click=on_channel_selected,
            ),
            width=2,
            when="channel_exists",
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
    ),
    # Окно настройки канала
    Window(
        Format("{channel_settings_desc}"),
        SwitchTo(
            text=Format("{channel_delete_from_bot_desc}"),
            id="delete_channel_selected",
        ),
        Button(
            text=Format("{channel_add_caption_desc}"),
            id="add_caption_channel",
            on_click=add_caption_to_channel,
        ),
        state=AdditionToChannelSG.channel_settings,
        getter=get_channel_settings,
    ),
    # Окно удаления канала из бота
    Window(
        Format({"{delete_bot_from_channel_desc}"}),
        Button(
            text=Format("{channe_delete_button}"),
            id="delete_channel_done",
            on_click=delete_channel_from_bot,
        ),
        Back(text=Format("{back}")),
        state=AdditionToChannelSG.delete_bot_from_channel,
        getter=get_data_for_delete,
    ),
)
