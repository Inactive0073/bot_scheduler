import logging
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import MessageInput, ManagedTextInput

from fluentogram import TranslatorRunner

from typing import TYPE_CHECKING

from app.bot.states.customer.start import StartCustomerSG
from app.bot.db.customer_requests import record_personal_user_data

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner  # type: ignore


logger = logging.getLogger(__name__)

async def process_succes_contact(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
):
    """Обрабатывает отправленный контакт и формирует диалог дату для дальнейшего сохранения в БД"""
    dialog_manager.dialog_data["phone"] = message.contact.phone_number
    await message.delete()
    await dialog_manager.switch_to(
        state=StartCustomerSG.name, show_mode=ShowMode.DELETE_AND_SEND
    )


async def process_invalid_phone(
    message: Message,
    message_input: MessageInput,
    dialog_manager: DialogManager,
):
    """Обрабатывает неправильный ввод данных"""
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")
    await message.delete()
    await message.answer(i18n.customer.error.phone())


async def process_succes_name(
    message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str
):
    await message.delete()
    dialog_manager.dialog_data["name"] = text
    await dialog_manager.switch_to(state=StartCustomerSG.surname, show_mode=ShowMode.DELETE_AND_SEND)



async def process_succes_surname(
    message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str
):
    await message.delete()
    dialog_manager.dialog_data["surname"] = text
    await dialog_manager.switch_to(state=StartCustomerSG.email, show_mode=ShowMode.DELETE_AND_SEND)



async def process_succes_email(
    message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str
):
    await message.delete()
    dialog_manager.dialog_data["email"] = text
    await dialog_manager.switch_to(state=StartCustomerSG.birthday, show_mode=ShowMode.DELETE_AND_SEND)



async def process_succes_birthday(
    message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str
):
    await message.delete()
    dialog_manager.dialog_data["birthday"] = text
    await dialog_manager.switch_to(state=StartCustomerSG.gender, show_mode=ShowMode.DELETE_AND_SEND)


async def process_invalid_birthday(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    error: ValueError,
):
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")
    await message.answer(i18n.customer.error.birthday())
    await message.delete()


async def process_gender_selected(
    callback: CallbackQuery, widget: Button, dialog_manager: DialogManager
):
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")
    session = dialog_manager.middleware_data.get("session")
    dialog_manager.dialog_data["gender"] = callback.data
    await callback.answer(i18n.customer.meeting.thanks())

    # Сохранение введеных данных в БД
    telegram_id = callback.from_user.id
    name = dialog_manager.dialog_data.get("name")
    surname = dialog_manager.dialog_data.get("surname")
    phone = dialog_manager.dialog_data.get("phone")
    email = dialog_manager.dialog_data.get("email")
    birthday = dialog_manager.dialog_data.get("birthday")
    gender = dialog_manager.dialog_data.get("gender", 'N')[0]
    
    if await record_personal_user_data(
            session=session,
            telegram_id=telegram_id,
            name=name,
            surname=surname,
            phone=phone,
            email=email,
            birthday=birthday,
            gender=gender
        ):
        logger.info(f"Запись успешно добавлена по юзеру {phone}")
        await dialog_manager.switch_to(state=StartCustomerSG.menu)
    else:
        logger.error(f"Не удалось добавить запись при регистрации клиента")
        

async def on_balance_selected(
    callback: CallbackQuery, widget: Button, dialog_manager: DialogManager
):
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")
    session = dialog_manager.middleware_data.get("session")
    