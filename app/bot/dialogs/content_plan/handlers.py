from datetime import date

from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager


async def on_date_selected(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, selected_date: date):
    await callback.answer(str(selected_date))