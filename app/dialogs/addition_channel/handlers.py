import logging
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery

from typing import TYPE_CHECKING

from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import TextInput
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.requests import delete_channel, upsert_channel
from app.states.addition_channel import AdditionToChannelSG

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner  # type: ignore

logger = logging.getLogger(__name__)


def validate_channel(text: str):
    """Проверяет корректность формата ввода для username или ссылки на канал.

    Возвращает очищенный username канала. Вызывает ValueError при неверном формате.
    """
    channel_name = text.startswith("@")
    link = text.find("https://t.me/")
    if not channel_name and link == -1:
        raise ValueError

    if link == -1:
        return text
    else:
        return text[text.find("@") :]


async def on_invalid_channel(
    message: Message, widget: TextInput, dialog_manager: DialogManager, err: ValueError
):
    """Отправляет сообщение о неверном формате канала и удаляет исходное сообщение."""

    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    await message.answer(i18n.channel.link.invalid())
    await message.delete()


async def check_admin_status(
    message: Message,
    widget: TextInput,
    dialog_manager: DialogManager,
    text: str,
):
    """Основной хэндлер для проверки прав бота и сохранения канала в БД.

    Получает информацию о канале через Telegram API, проверяет тип чата,
    сохраняет данные в базу и отправляет подтверждение пользователю.
    """
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")
    bot: Bot = dialog_manager.middleware_data.get("bot")
    session: AsyncSession = dialog_manager.middleware_data.get("session")
    try:
        chat_full_info = await bot.get_chat(chat_id=text)
    except TelegramBadRequest:
        await message.answer(i18n.channel.link.invalid())
        return

    if chat_full_info.type in ("private", "group", "supergroup"):
        await message.answer(i18n.channel.link.wrong.type())
        return

    await upsert_channel(
        session=session,
        channel_id=chat_full_info.id,
        channel_name=chat_full_info.title,
        channel_username=chat_full_info.username,
        channel_link=chat_full_info.invite_link,
        admin_id=message.from_user.id,
    )
    await message.answer(i18n.channel.link.after.joining.channel())
    await message.delete()


async def on_channel_selected(
    callback: CallbackQuery, widget: Button, dialog_manager: DialogManager, item_id: str
):
    dialog_manager.dialog_data["channel_selected_id"] = item_id
    await dialog_manager.switch_to(
        state=AdditionToChannelSG.channel_settings, show_mode=ShowMode.DELETE_AND_SEND
    )


async def delete_channel_from_bot(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
):
    """Хендлер для удаления канала из бота"""
    channel_id = dialog_manager.dialog_data["channel_selected_id"]
    bot: Bot = dialog_manager.middleware_data.get("bot")
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")
    session: AsyncSession = dialog_manager.middleware_data.get("session")

    if await bot.leave_chat(channel_id):
        await callback.answer(i18n.channel.success.deleted())
        await delete_channel(session=session, channel_id=channel_id)
        dialog_manager.switch_to(
            state=AdditionToChannelSG.channel_settings,
            show_mode=ShowMode.DELETE_AND_SEND,
        )
    else:
        logger.error(f"Произошла ошибка бот не был удален из канала: {channel_id}.")
        await callback.answer(i18n.channel.unsuccessful.deleted())


async def add_caption_to_channel(
    callback: CallbackQuery, widget: Button, dialog_manager: DialogManager
):
    """Хендлер для добавления автоподписи к боту"""
    ...
