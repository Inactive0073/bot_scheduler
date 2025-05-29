from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from app.bot.db.manager_requests import set_user_tz
from app.bot.states.manager.manager import ManagerSG


async def back_to_menu(
    callback: CallbackQuery, _: Button, dialog_manager: DialogManager
) -> None:
    is_admin = dialog_manager.start_data.get("is_admin")
    await dialog_manager.start(state=ManagerSG.start, data={"is_admin": is_admin})
    

async def on_timezone_selected(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
    timezone_data: str,
):
    timezone, tz_offset = timezone_data.split("|")
    tz_offset = int(tz_offset)
    session = dialog_manager.middleware_data.get("session")
    dialog_manager.dialog_data["user_timezone"] = timezone_data
    dialog_manager.dialog_data["tz_offset"] = tz_offset
    await set_user_tz(
        session=session,
        telegram_id=callback.from_user.id,
        tz_offset=tz_offset,
        timezone=timezone,
    )
