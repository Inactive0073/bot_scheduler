from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import WebApp, Button, Group, SwitchTo
from aiogram_dialog.widgets.input import TextInput

from ...states.waiter.start import WaiterSG
from .getters import get_common_data, get_processing_guest_data
from .handlers import process_qr_token

waiter_dialog = Dialog(
    Window(
        Format("{hello_waiter}"),
        WebApp(Format("{waiter_menu_scan}"), url=Format("{waiter_menu_scan_url}")),
        TextInput(id="process_qr_token", type_factory=int, on_success=process_qr_token),
        state=WaiterSG.start,
    ),
    Window(
        Format("{process_guest_message}"),
        Group(
            SwitchTo(
                Format("{add_bonus_button}"), 
                id="on_add_selected", 
                state=WaiterSG.adding),
            SwitchTo(
                Format("{subtract_bonus_button}"), 
                id="on_subtract_selected", 
                state=WaiterSG.subtracting),
            width=2
        ),
        SwitchTo(Format("{back}"), id="__back__", state=WaiterSG.start),
        state=WaiterSG.processing,
        getter=get_processing_guest_data
    ),
    Window(
        Format("{adding_instruction}"),
        TextInput(id="adding_bonus_amount", on_success=...),
        state=WaiterSG.adding,
        getter=get_processing_guest_data
    ),
    Window(
        Format("{subtracting_instruction}"),
        TextInput(id="subtracting_bonus_amount", on_success=...),
        state=WaiterSG.subtracting,
        getter=get_processing_guest_data
    ),
    getter=get_common_data,
)
