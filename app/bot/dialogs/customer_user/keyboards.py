from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_kb(data: list[str, str], width=1) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.adjust(width)
    for text, url in data:
        builder.add(InlineKeyboardButton(text=text, url=url))
    return builder.as_markup()
