from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup

from .broker import broker


@broker.task
async def send_scheduled_message_to_channel(
    bot: Bot,
    channel_id: str,
    text: str,
    kb: InlineKeyboardMarkup = None,
    media: str = None,
):
    if media is None:
        await bot.send_message(chat_id=channel_id, text=text, reply_markup=kb)
    elif media:
        await bot.send_photo(
            chat_id=channel_id, photo=..., caption=text, reply_markup=kb
        )
