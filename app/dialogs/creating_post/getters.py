from typing import TYPE_CHECKING, Dict

from aiogram.types import User

from aiogram_dialog import DialogManager

from dataclasses import dataclass

from fluentogram import TranslatorRunner

from app.db.requests import get_channels

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner  # type:ignore


@dataclass
class NotifyAlert:
    id: str
    desc: str


async def get_posting_sg_common_data(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> Dict[str, str]:
    return {
        "cancel_caption": i18n.cancel(),
        "yes_caption": i18n.yes(),
    }


async def get_watch_text(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> Dict[str, str]:
    return {
        "watch_text": i18n.cr.watch.text(),
    }


async def get_creating_post_data(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> Dict[str, str]:
    content_msg = dialog_manager.dialog_data.get("post_message", "Сообщение не найдено")
    url_button_empty = dialog_manager.dialog_data.get("url_button_empty", True)

    posting_time = dialog_manager.dialog_data.get("dt_posting_view", None)
    posting_time_index = bool(posting_time)
    has_media = dialog_manager.dialog_data.get("has_media", False)
    has_keyboard = dialog_manager.dialog_data.get("has_keyboard", False)
    notify_status = dialog_manager.dialog_data.get("notify_status", True)

    return {
        "reply_title": i18n.cr.reply.text(),
        "post_message": content_msg,
        "edit": i18n.cr.edit.text(),
        "url": i18n.cr.url.btns(),
        "url_delete": i18n.cr.url.delete(),
        "set_time": i18n.cr.set.time(),
        "posting_time": posting_time,
        "posting_time_index": posting_time_index,
        "states_notify": [
            NotifyAlert(id="turn_on", desc=i18n.cr.set.notify()),
            NotifyAlert(id="turn_off", desc=i18n.cr.unset.notify()),
        ],
        "notify_status": notify_status,
        "media_message": i18n.cr.add.media(),
        "delete_media_message": i18n.cr.remove.media(),
        "has_media": has_media,
        "has_keyboard": has_keyboard,
        "unset_comments": i18n.cr.unset.comments(),
        "push_now": i18n.cr.push.now(),
        "push_later": i18n.cr.push.later(),
        "url_button_empty": url_button_empty,
        "url_button_exists": not url_button_empty,
    }


async def get_url_instruction(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> Dict[str, str]:
    return {
        "instruction_url": i18n.cr.instruction.url(),
    }


async def get_time_instruction_data(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> Dict[str, str]:
    return {"instruction_delayed_post": i18n.cr.instruction.delayed.post()}


async def get_addition_media_data(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> Dict[str, str]:
    return {
        "instruction_add_media": i18n.cr.instruction.media.post(),
    }


async def get_approve_push_data(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> Dict[str, str]:
    return {
        "push_now_approve_message": i18n.cr.approve.media.now(),
    }
    

async def get_preselect_channel_data(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> Dict[str, str]:
    session = dialog_manager.middleware_data.get("session")
    telegram_id = event_from_user.id
    channels = await get_channels(session=session, telegram_id=telegram_id)
    
    return {
        "push_now_approve_message": i18n.cr.approve.media.now(),
        "channels": channels,
    }