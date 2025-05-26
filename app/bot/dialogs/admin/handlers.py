from datetime import datetime
import logging
from aiogram import Bot
from aiogram.types import (
    Message,
    CallbackQuery,
    BufferedInputFile,
)
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import MessageInput, ManagedTextInput

from fluentogram import TranslatorRunner

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from locales.stub import TranslatorRunner  # type: ignore


logger = logging.getLogger(__name__)


async def process_username_or_id(
    message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str
):
    pass