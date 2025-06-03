from datetime import date
from typing import TYPE_CHECKING, Callable

from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from app.bot.db.message_requests import cancel_post
from app.bot.states.manager.content import ContentSG
from taskiq_nats import NATSKeyValueScheduleSource

import logging

from app.bot.utils.enums.message import MessageType
from app.bot.utils.schemas.models import PostData

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner  # type: ignore

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
    dialog_manager.dialog_data["schedule_id"] = schedule_id
    await dialog_manager.switch_to(ContentSG.process_selected)
    
async def on_cancel_selected(
    callback: CallbackQuery, _: Button, dialog_manager: DialogManager
):
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")
    session = dialog_manager.middleware_data.get("session")
    nats_source: NATSKeyValueScheduleSource = dialog_manager.middleware_data.get("nats_source")

    schedule_id = dialog_manager.dialog_data.get("schedule_id")
    filter_item = Callable[[dict], bool] = lambda item: item["schedule_id"] != schedule_id

    try:
        nats_source.delete_schedule(schedule_id)

        if await cancel_post(session=session,schedule_id=schedule_id):
            await callback.message.answer(i18n.content.successfull.deleted())
            dialog_manager.dialog_data["selected_date"] = None
            if dialog_manager.dialog_data.get(MessageType.BOT):
                await dialog_manager.switch_to(ContentSG.today_info_bot)
                print(f"После чистки: {dialog_manager.dialog_data["parsed_posts"]}")
                dialog_manager.dialog_data["parsed_posts"] = list(filter(filter_item, dialog_manager.dialog_data.get("parsed_posts")))
                print(f"После чистки: {dialog_manager.dialog_data["parsed_posts"]}")
            elif dialog_manager.dialog_data.get(MessageType.CHANNEL):
                await dialog_manager.switch_to(ContentSG.today_info_channel)

        else:
            raise ValueError(f"Не удалось отменить пост {schedule_id}.")
    except Exception as e:
        await callback.message.answer(i18n.content.unsuccessful.deleted())
        logger.error(f"Произошла ошибка в обработке отмены поста.")
    