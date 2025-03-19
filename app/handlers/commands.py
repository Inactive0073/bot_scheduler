from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from sqlalchemy.ext.asyncio import AsyncSession

from app.states.start import StartSG
from app.states.options import OptionsSG
from app.db.requests import upsert_user

commands_router = Router(name=__name__)


@commands_router.message(CommandStart())
async def process_start_command(
    message: Message,
    dialog_manager: DialogManager,
    session: AsyncSession,
) -> None:
    await upsert_user(
        session=session,
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)


@commands_router.message(Command("demo"))
async def process_demo_command(
    message: Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(state=StartSG.demo)


@commands_router.message(Command("cancel"))
async def process_cancel_command(
    message: Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(state=OptionsSG.cancel)
