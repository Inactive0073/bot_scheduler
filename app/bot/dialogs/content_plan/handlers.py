from datetime import date

from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from app.bot.states.manager.content import ContentSG

import logging

logger = logging.getLogger(__name__)

async def on_date_selected(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, selected_date: date):
    dialog_manager.dialog_data["selected_date"] = selected_date
    logger.debug(f"Пользователь {callback.from_user.id} выбрал {selected_date} для отображения запланированных постов.")
    await dialog_manager.switch_to(ContentSG.today_info_bot)
    

async def type_selected(
    callback: CallbackQuery, _: Button, dialog_manager: DialogManager
):
    dialog_manager.dialog_data["recipient_type"] = callback.data