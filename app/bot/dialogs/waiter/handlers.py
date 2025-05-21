from typing import TYPE_CHECKING

from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    CallbackQuery,
    InputMediaPhoto,
)
from aiogram.exceptions import TelegramBadRequest

from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import Button, Toggle, Multiselect, ManagedMultiselect

from app.bot.db.models.customers import Customer
from app.bot.db.customer_requests import get_bonus_info, get_customer_detail_info
from ...states.waiter.start import WaiterSG

import logging

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner  # type: ignore

logger = logging.getLogger(__name__)

async def process_qr_token(
    message: Message,
    widget: TextInput,
    dialog_manager: DialogManager,
    token: int
) -> None:
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")
    session = dialog_manager.middleware_data.get("session")
    
    customer = await get_customer_detail_info(session=session, qr_code_token=token)
    result = await get_bonus_info(session=session, telegram_id=customer.telegram_id)
    
    if result:
        bonuses, date_expire, bonus_to_expire = result
        text = i18n.waiter.success.info.customer(
            name=customer.i_name, balance=bonuses, date_expire=date_expire, bonus_to_expire=bonus_to_expire
        )
        await message.answer(text=text)
        await dialog_manager.switch_to(WaiterSG.processing)
    else:
        text = i18n.waiter.invalid.info.customer()
        await message.answer(text=text)
    
    
        