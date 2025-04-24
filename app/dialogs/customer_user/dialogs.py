from aiogram import F
from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window, ShowMode
from aiogram_dialog.widgets.text import Format, Case, List
from aiogram_dialog.widgets.kbd import (
    Group,
    SwitchTo,
    Toggle,
    Button,
    Multiselect,
    Row,
    Start,
)
from aiogram_dialog.widgets.input import TextInput, MessageInput
from app.states.customer.start import StartCustomerSG

customer_dialog = Dialog(
    Window(state=StartCustomerSG.start),
    getter=...,
)
