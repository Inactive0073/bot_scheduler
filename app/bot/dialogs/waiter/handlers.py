from typing import TYPE_CHECKING

from aiogram.types import (
    Message,
)

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput

from app.bot.db.models.customers import Customer
from app.bot.db.customer_requests import (
    get_bonus_info,
    get_customer_detail_info,
    add_bonus,
    deduct_bonus,
)
from ...states.waiter.start import WaiterSG

import logging

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner  # type: ignore

logger = logging.getLogger(__name__)


async def process_qr_token(
    message: Message, widget: TextInput, dialog_manager: DialogManager, token: int
) -> None:
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")
    session = dialog_manager.middleware_data.get("session")

    customer: Customer = await get_customer_detail_info(
        session=session, qr_code_token=token
    )

    if customer:
        result = await get_bonus_info(session=session, telegram_id=customer.telegram_id)
        bonuses, date_expire, bonus_to_expire = result
        date_expire = "♾" if date_expire is None else date_expire

        dialog_manager.dialog_data["has_bonus"] = bool(date_expire)
        dialog_manager.dialog_data["customer_id"] = customer.telegram_id
        dialog_manager.dialog_data["customer_balance"] = bonuses

        text = i18n.waiter.success.info.customer(
            name=customer.i_name,
            balance=bonuses,
            date_expire=date_expire,
            bonus_to_expire=bonus_to_expire,
        )
        await message.answer(text=text)
        await dialog_manager.switch_to(WaiterSG.processing)
    else:
        text = i18n.waiter.invalid.info.customer()
        await message.answer(text=text)


async def process_adding_bonus(
    message: Message,
    widget: TextInput,
    dialog_manager: DialogManager,
    total_amount: int,
) -> None:
    session = dialog_manager.middleware_data.get("session")
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")

    customer_id = dialog_manager.dialog_data.get("customer_id")
    amount_bonus = await add_bonus(
        session=session, customer_id=customer_id, total_amount=total_amount
    )
    if amount_bonus != False:
        text = i18n.waiter.processing.adding.success(amount=amount_bonus)
        await message.answer(text)
        await dialog_manager.switch_to(WaiterSG.start)
    else:
        text = i18n.waiter.processing.adding.unsuccess()
        await message.answer(text)
        logger.info(f"Не удалось начислить баллы для юзера {customer_id}")


async def process_subtract_bonus(
    message: Message, widget: TextInput, dialog_manager: DialogManager, n_bonus: int
) -> None:
    session = dialog_manager.middleware_data.get("session")
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")

    customer_id = dialog_manager.dialog_data.get("customer_id")
    customer_balance = dialog_manager.dialog_data.get("customer_balance")
    if customer_balance < n_bonus:
        await message.answer(i18n.waiter.processing.subtracting.not_.enough())
        return

    result = await deduct_bonus(
        session=session, customer_id=customer_id, amount=n_bonus
    )
    if result != False:
        text = i18n.waiter.processing.subtracting.success()
        await message.answer(text)
        await dialog_manager.switch_to(WaiterSG.start)
    else:
        text = i18n.waiter.processing.subtracting.unsuccess()
        await message.answer(text)
