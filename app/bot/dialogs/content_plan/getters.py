from typing import TYPE_CHECKING, Dict

from aiogram.types import User

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Multiselect
from app.bot.db.manager_requests import get_user_tz

from fluentogram import TranslatorRunner

from datetime import timedelta, datetime, timezone, date

from app.bot.db.message_requests import get_posts
from app.bot.utils.enums import MessageType
from .services import find_today_posts, parse_post_data


if TYPE_CHECKING:
    from locales.stub import TranslatorRunner  # type:ignore
    
months = {
        1: "январь",
        2: "февраль",
        3: "март",
        4: "апрель",
        5: "май",
        6: "июнь",
        7: "июль",
        8: "август",
        9: "сентябрь",
        10: "октябрь",
        11: "ноябрь",
        12: "декабрь",
}


async def content_data(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    **kwargs,
) -> Dict[str, str]:
    return {
        "main_menu": i18n.main.menu(),
        "content_hello_msg": i18n.content.hello(),
        "content_bot_btn": i18n.content.bot.btn(),
        "content_channel_btn": i18n.content.channel.btn(),
        "delete_btn": i18n.delete(),
        "edit_btn": i18n.edit(),
    }
    
    
async def content_bot_data(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> Dict[str, str]:
    
    session = dialog_manager.middleware_data.get("session")
    all_posts = await get_posts(session=session, target_type=MessageType.BOT)
    _ , user_tz_offset = await get_user_tz(session=session, telegram_id=event_from_user.id)
    
    idx_month = datetime.now(tz=timezone(timedelta(hours=user_tz_offset))).month
    current_month = months[idx_month]
    parsed_data = parse_post_data(all_posts)
    
    dialog_manager.dialog_data["user_tz_offset"] = user_tz_offset
    dialog_manager.dialog_data["parsed_posts"] = parsed_data

    text_month_info = i18n.content.month.info.msg(month=current_month, count_post=len(parsed_data))

    return {
        "bot_content_msg": text_month_info,
        "back": i18n.back(),
    }


async def content_today_bot_data(
        dialog_manager: DialogManager,
        i18n: TranslatorRunner,
        **kwargs,
) -> Dict[str,str]:
    user_tz_offset = dialog_manager.dialog_data.get("user_tz_offset")
    parsed_posts = dialog_manager.dialog_data.get("parsed_posts")

    today_posts = find_today_posts(parsed_posts, user_tz_offset)
    today_dt = datetime.now().

    text_today_info = i18n.content.today.info.msg(today=..., count_post=...)


async def content_channel_data(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs,
) -> Dict[str, str]:
    session = dialog_manager.middleware_data.get("session")
    all_posts = await get_posts(session=session, target_type=MessageType.CHANNEL)
    _ , user_tz_offset = await get_user_tz(session=session, telegram_id=event_from_user.id)
    
    idx_month = datetime.now(tz=timezone(timedelta(hours=user_tz_offset))).month
    current_month = months[idx_month]
    parsed_data = parse_post_data(all_posts)
    
    text_month_info = i18n.content.month.info.msg(month=current_month, count_post=len(parsed_data))
    
    return {
        "channel_content_msg": text_month_info,
        "back": i18n.back(),
    }


async def content_today_channel_data(
        dialog_manager: DialogManager,
        i18n: TranslatorRunner,
        **kwargs,
) -> Dict[str,str]:
    pass