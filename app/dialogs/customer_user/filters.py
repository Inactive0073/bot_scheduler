from aiogram.filters import BaseFilter
from aiogram.types import Message, Contact


class ContactFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return (
            message.chat.type == "contact"
            and message.contact.user_id == message.chat.id
        )
