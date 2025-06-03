from datetime import date

from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from app.bot.db.message_requests import cancel_post
from app.bot.states.manager.content import ContentSG
from taskiq_nats import NATSKeyValueScheduleSource

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
    
    
async def on_post_selected(
    callback: CallbackQuery, _: Button, dialog_manager: DialogManager, schedule_id: str
):
    nats_source: NATSKeyValueScheduleSource = dialog_manager.middleware_data.get("nats_source")
    session = dialog_manager.middleware_data.get("session")
    try:
        nats_source.delete_schedule(schedule_id)
        if await cancel_post(session=session,schedule_id=schedule_id):
            await callback.message.answer()
    except Exception as e:
        pass
    