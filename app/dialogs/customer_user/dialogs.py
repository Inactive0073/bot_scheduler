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
    RequestContact,
)
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory

from app.states.customer.start import StartCustomerSG
from .getters import get_common_data
from .filters import ContactFilter
from .handlers import (
    process_gender_selected,
    process_invalid_birthday,
    process_invalid_phone,
    process_succes_birthday,
    process_succes_contact,
    process_succes_email,
    process_succes_name,
    process_succes_surname,
)
from .services import check_birthday_format

customer_dialog = Dialog(
    Window(
        Format("{hello_guest}"),
        RequestContact(Format("{meeting_phone_message}")),
        MessageInput(
            func=process_succes_contact,
            content_types=ContentType.CONTACT,
            filter=ContactFilter,
        ),
        MessageInput(func=process_invalid_phone, content_types=ContentType.ANY),
        state=StartCustomerSG.start,
        markup_factory=ReplyKeyboardFactory(
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
    ),
    Window(
        Format("{meeting_name_message}"),
        TextInput(
            id="expecting_name",
            on_success=process_succes_name,
        ),
        state=StartCustomerSG.name,
    ),
    Window(
        Format("{meeting_surname_message}"),
        TextInput(
            id="expecting_surname",
            on_success=process_succes_surname,
        ),
        state=StartCustomerSG.surname,
    ),
    Window(
        Format("{meeting_email_message}"),
        TextInput(id="expecting_name", on_success=process_succes_email),
        state=StartCustomerSG.email,
    ),
    Window(
        Format("{meeting_birthday_message}"),
        TextInput(
            id="expecting_name",
            on_success=process_succes_birthday,
            type_factory=check_birthday_format,
            on_error=process_invalid_birthday,
        ),
        state=StartCustomerSG.birthday,
    ),
    Window(
        Format("{meeting_gender_message}"),
        Row(
            Button(Format("{meeting_gender_m_button}"), id="m_gender_selected", on_click=process_gender_selected),
            Button(Format("{meeting_gender_f_button}"), id="f_gender_selected", on_click=process_gender_selected),
            ),
        state=StartCustomerSG.gender,
    ),
    getter=get_common_data,
)
