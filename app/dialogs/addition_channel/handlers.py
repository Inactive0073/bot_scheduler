from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from typing import TYPE_CHECKING

from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import TextInput
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.requests import upsert_channel

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner  # type: ignore

def validate_channel(text: str):
    channel_name = text.startswith("@")
    link = text.find("https://t.me/")
    if not channel_name and link == -1:
        raise ValueError

    if link == -1:
        return text
    else:
        return text[text.find("@"):]

async def on_invalid_channel(
    message: Message,
    widget: TextInput,
    dialog_manager:DialogManager,
    err: ValueError
):
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
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")
    bot: Bot = dialog_manager.middleware_data.get("bot")
    session: AsyncSession = dialog_manager.middleware_data.get("session")
    try:
        chat_full_info = await bot.get_chat(chat_id=text)
    except TelegramBadRequest:
        await message.answer(i18n.channel.link.invalid())
        return
    
    if chat_full_info.type in ('private', 'group', 'supergroup'):
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
    dialog_manager.dialog_data['channel_exists'] = True
    
    