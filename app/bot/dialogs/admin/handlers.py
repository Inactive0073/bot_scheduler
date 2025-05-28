from datetime import datetime
import logging
from aiogram import Bot
from aiogram.types import (
    Message,
    CallbackQuery,
    BufferedInputFile,
)
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.input import MessageInput, ManagedTextInput

from fluentogram import TranslatorRunner

from typing import TYPE_CHECKING

from app.bot.db.admin_requests import create_employee
from app.bot.db.common_requests import get_telegram_id_by_username
from app.bot.states.admin.admin import AdminSG
from app.bot.utils.exc import AlreadyHaveAllRoles, NotFoundError


if TYPE_CHECKING:
    from locales.stub import TranslatorRunner  # type: ignore


logger = logging.getLogger(__name__)


async def process_to_select_role(
    callback: CallbackQuery, _: Select, dialog_manager: DialogManager, data: str
):
    dialog_manager.dialog_data["selected_role"] = data
    await dialog_manager.switch_to(AdminSG.invite)

async def process_username_or_id(
    message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str
):
    session = dialog_manager.middleware_data.get("session")
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")
    role = dialog_manager.dialog_data.get("selected_role")

    if not text.isdigit():
        telegram_id = await get_telegram_id_by_username(session=session, username=text)
        if telegram_id is None:
            await message.answer(i18n.admin.not_.found.user())
            return
    else:
        telegram_id = text
    telegram_id = int(telegram_id)
    logger.info(f"Получен запрос на добавлении нового пользователя {telegram_id} с ролью {role}.")
    try:
        result = await create_employee(session=session, telegram_id=telegram_id, role=role)
        if result:
            await message.answer(i18n.admin.team.invite.success())
            await dialog_manager.switch_to(AdminSG.start)
        else:
            await message.answer(i18n.admin.team.invite.unsuccess())
    except NotFoundError:
        await message.answer(i18n.admin.not_.found.user())
    except AlreadyHaveAllRoles:
        await message.answer(i18n.admin.team.already.has.roles())