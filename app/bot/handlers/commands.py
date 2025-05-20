import logging
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode, StartMode

from sqlalchemy.ext.asyncio import AsyncSession


from ..db.customer_requests import has_customer_detail_info, upsert_customer
from ..states.customer.start import CustomerSG
from ..states.settings import SettingsSG
from ..states.start import StartSG
from ..states.waiter.start import WaiterSG
from ..db.requests import upsert_user
from ..db.common_requests import get_user_role

commands_router = Router(name=__name__)

logger = logging.getLogger(__name__)


@commands_router.message(CommandStart())
async def process_start_command(
    message: Message,
    dialog_manager: DialogManager,
    session: AsyncSession,
) -> None:
    username = message.from_user.username
    telegram_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    roles = set(await get_user_role(session=session, telegram_id=telegram_id))
    logger.info(
        f"Пользователь {first_name}|{username} с ролями {roles}, нажал кнопку /start"
    )

    if not roles.intersection({"admin", "manager", "waiter", "owner"}):
        if not (await has_customer_detail_info(session, telegram_id)):
            logger.debug(f"Проверка пройдена успешно!")
            await upsert_customer(
                session=session,
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
            )
            logger.debug(f"Обновление данных пройдено успешно")
            await dialog_manager.start(
                state=CustomerSG.start, mode=StartMode.RESET_STACK
            )
        else:
            await dialog_manager.start(
                state=CustomerSG.menu, show_mode=ShowMode.DELETE_AND_SEND
            )
    else:
        await upsert_user(
            session=session,
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        if "manager" in roles:
            await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)
        elif "waiter" in roles:
            await dialog_manager.start(state=WaiterSG.start, mode=StartMode.RESET_STACK)

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
    await dialog_manager.back(show_mode=ShowMode.DELETE_AND_SEND)


@commands_router.message(Command("settings"))
async def process_settings_command(
    message: Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(state=SettingsSG.start)
