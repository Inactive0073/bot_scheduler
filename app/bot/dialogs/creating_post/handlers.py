from typing import TYPE_CHECKING

from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    CallbackQuery,
    InputMediaPhoto,
)
from aiogram.exceptions import TelegramBadRequest

from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import Button, Toggle, Multiselect, ManagedMultiselect

from app.bot.db.customer_requests import get_all_customers
from app.bot.db.message_requests import upsert_post
from app.bot.db.manager_requests import get_user_tz
from app.bot.dialogs.creating_post.services import get_delay
from app.bot.states.manager.creating_post import PostingSG

from datetime import datetime, timezone, timedelta

from logging import getLogger

from app.tasks import (
    send_message_bot_subscribers,
    send_schedule_message_bot_subscribers,
    send_message_to_channel,
)

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner  # type: ignore

logger = getLogger(__name__)


async def process_to_select_bot_mailing(
    message: Message, widget: Button, dialog_manager: DialogManager
) -> None:
    """Сеттер для типа получателя бот"""
    logger.info(
        "Пользователь выбрал рассылку по ботам",
        extra={"user_id": message.from_user.id, "action": "select_bot_mailing"},
    )
    dialog_manager.dialog_data["recipient_type"] = "bot"


async def process_to_select_channel(
    message: Message, widget: ManagedMultiselect, dialog_manager: DialogManager, data
) -> None:
    """Сеттер для типа получателя канал"""
    logger.info(
        "Пользователь выбрал отправку в каналы",
        extra={"user_id": message.from_user.id, "action": "select_channel"},
    )
    dialog_manager.dialog_data["recipient_type"] = "channel"


# Запись поста
async def process_post_msg(
    message: Message, widget: MessageInput, dialog_manager: DialogManager
) -> None:
    """Обработчик сообщения с постом пользователя.
    Сохраняет сообщение в dialog_data для дальнейшей репрезентации пользователю
    и осуществляет переход в следующее окно.
    """
    logger.info(
        "Пользователь создает новый пост",
        extra={
            "user_id": message.from_user.id,
            "action": "create_post",
            "message_type": message.content_type,
        },
    )
    try:
        copy_msg = await message.send_copy(chat_id=message.chat.id)
        dialog_manager.dialog_data.update(
            {
                "post_message": copy_msg.text,
                "chat_id": copy_msg.chat.id,
                "message_id": copy_msg.message_id,
            }
        )
        logger.debug(
            "Пост успешно сохранен",
            extra={
                "user_id": message.from_user.id,
                "message_id": copy_msg.message_id,
                "text_preview": copy_msg.text[:50] if copy_msg.text else "Нет текста",
            },
        )
    except Exception as e:
        logger.error(
            "Ошибка при создании поста",
            extra={
                "user_id": message.from_user.id,
                "error": str(e),
                "error_type": type(e).__name__,
            },
            exc_info=True,
        )
        raise
    # удаляем старое сообщение, чтобы сохранить историю чище
    await message.bot.delete_message(
        chat_id=message.chat.id, message_id=message.message_id
    )

    await dialog_manager.switch_to(
        state=PostingSG.creating_post, show_mode=ShowMode.DELETE_AND_SEND
    )


async def process_other_type_msg(
    message: Message, widget: MessageInput, dialog_manager: DialogManager
) -> None:
    """
    Обрабатывает сообщения с неподдерживаемыми типами контента.

    Отправляет пользователю сообщение о недопустимом формате данных.
    Используется для фильтрации нежелательных типов ввода (не текст/фото).
    """
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")
    await message.answer(i18n.cr.invalid.data())


# Добавления URL кнопок
async def process_button_case(
    message: Message,
    widget: TextInput,
    dialog_manager: DialogManager,
    keyboard: InlineKeyboardMarkup,
) -> None:
    """
    Обрабатывает ввод пользователя для добавления URL-кнопок к сообщению.

    Обновляет исходное сообщение, добавляя к нему инлайн-клавиатуру.
    Использует данные из dialog_data для редактирования сообщения.

    """
    logger.info(
        "Пользователь добавляет URL-кнопки",
        extra={
            "user_id": message.from_user.id,
            "action": "add_url_buttons",
            "message_id": dialog_manager.dialog_data.get("message_id"),
        },
    )
    try:
        # Получаем данные из dialog_data для создания кнопки
        msg_id = dialog_manager.dialog_data["message_id"]
        chat_id = dialog_manager.dialog_data["chat_id"]
        post_message = dialog_manager.dialog_data["post_message"]
        media_file_id = dialog_manager.dialog_data.get("media_content")

        # Кладем клавиатуру в dialog_data
        dialog_manager.dialog_data["keyboard"] = keyboard.model_dump()

        # добавляем сообщению кнопки
        if dialog_manager.dialog_data.get("media_content") is None:
            await message.bot.edit_message_text(
                text=post_message,
                chat_id=chat_id,
                message_id=msg_id,
                reply_markup=keyboard,
            )
        else:
            media = InputMediaPhoto(media=media_file_id, caption=post_message)
            await message.bot.edit_message_media(
                media=media,
                chat_id=chat_id,
                message_id=msg_id,
                reply_markup=keyboard,
            )

        # удаляем старое сообщение для чистой истории
        await message.bot.delete_message(
            chat_id=message.chat.id, message_id=message.message_id
        )

        logger.debug(
            "Кнопки успешно добавлены",
            extra={
                "user_id": message.from_user.id,
                "message_id": msg_id,
                "keyboard_count": len(keyboard.inline_keyboard),
            },
        )
    except Exception as e:
        logger.error(
            "Ошибка при добавлении кнопок",
            extra={
                "user_id": message.from_user.id,
                "error": str(e),
                "error_type": type(e).__name__,
            },
            exc_info=True,
        )
        raise

    logger.debug("Сообщение было отредактировано")

    # Сохраняем в dialog_data изменение кнопки
    dialog_manager.dialog_data["url_button_empty"] = False
    dialog_manager.dialog_data["url_button_exists"] = True

    await dialog_manager.switch_to(PostingSG.creating_post, ShowMode.DELETE_AND_SEND)


async def process_delete_button(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    """
    Удаляет кнопки с меню настройки постинга новости
    """
    msg = dialog_manager.dialog_data["post_message"]
    msg_id = dialog_manager.dialog_data["message_id"]
    media = dialog_manager.dialog_data.get("media_content")
    if media is None:
        await callback.message.bot.edit_message_text(
            text=msg,
            chat_id=callback.message.chat.id,
            message_id=msg_id,
        )
    else:
        media = InputMediaPhoto(media=media, caption=msg)
        await callback.message.bot.edit_message_media(
            media=media,
            chat_id=callback.message.chat.id,
            message_id=msg_id,
        )
    dialog_manager.dialog_data["url_button_empty"] = True
    dialog_manager.dialog_data["url_button_exists"] = False


async def process_invalid_button_case(
    message: Message,
    widget: TextInput,
    dialog_manager: DialogManager,
    e: ValueError,
):
    """
    Удаляет сообщения с неудачным текстом и инструкцией для чистой истории
    """
    await message.bot.delete_message(
        chat_id=message.chat.id, message_id=message.message_id - 1
    )
    await message.bot.delete_message(
        chat_id=message.chat.id, message_id=message.message_id
    )


# Редактирование текста
async def edit_text(
    message: Message, widget: TextInput, dialog_manager: DialogManager, text: str
):
    """
    Финализатор работы с добавлением кнопок к сообщению.
    """
    # получаем данные для редактирования сообщения
    msg_id = dialog_manager.dialog_data["message_id"]
    chat_id = dialog_manager.dialog_data["chat_id"]

    keyboard = dialog_manager.dialog_data.get("keyboard")

    # удаляем старое сообщение
    await message.bot.delete_message(
        chat_id=message.chat.id, message_id=message.message_id
    )

    # редактируем выбранное сообщение
    if keyboard:
        await message.bot.edit_message_text(
            text=text, message_id=msg_id, chat_id=chat_id, reply_markup=keyboard
        )

    else:
        await message.bot.edit_message_text(
            text=text,
            message_id=msg_id,
            chat_id=chat_id,
        )

    # Возвращаемся обратно в меню создания и настройки поста
    await dialog_manager.switch_to(
        PostingSG.creating_post, show_mode=ShowMode.DELETE_AND_SEND
    )


# Установка времени поста
async def process_set_time(
    message: Message, widget: TextInput, dialog_manager: DialogManager, dt: datetime
) -> None:
    """
    Сохраняет время публикации

    Допустимые форматы:
        18 - текущие сутки 18:00
        0830 - текущие сутки 08:30
        1830 - текущие сутки 18:30
        18300408 - 18:30 04.08
    """
    session = dialog_manager.middleware_data.get("session")
    tz, tz_offset = await get_user_tz(session, message.from_user.id)
    dt = dt.replace(
        tzinfo=timezone(timedelta(hours=tz_offset))
    )  # Устанавливаем часовой пояс из БД
    logger.info(
        f"Пользователь {message.from_user.username} устанавливает время публикации на {dt}"
    )
    try:
        weekday = ("пн", "вт", "ср", "чт", "пт", "сб", "вс")[dt.weekday()]
        dialog_manager.dialog_data["dt_posting_iso"] = dt.isoformat()
        dialog_manager.dialog_data["dt_posting_view"] = (
            f"{weekday}, {dt.strftime('%d.%m, %H:%M')}"
        )
        logger.debug(
            f"Время публикации установлено на {dialog_manager.dialog_data['dt_posting_view']}"
        )
    except Exception as e:
        logger.critical(f"Ошибка при установке времени публикации: {str(e)}")
        raise
    await message.delete()
    await dialog_manager.switch_to(
        PostingSG.creating_post, show_mode=ShowMode.DELETE_AND_SEND
    )


async def invalid_set_time(
    message: Message, widget: TextInput, dialog_manager: DialogManager, e: ValueError
) -> None:
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")
    session = dialog_manager.middleware_data.get("session")
    tz, tz_offset = await get_user_tz(session=session, telegram_id=message.from_user.id)
    await message.answer(i18n.cr.instruction.invalid.time(tz=tz))
    await message.delete()


# Установка медиа
async def process_addition_media(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    """
    Сохранение медиа
    """
    logger.info(
        "Пользователь добавляет медиа",
        extra={
            "user_id": message.from_user.id,
            "action": "add_media",
            "media_type": message.content_type,
        },
    )
    try:
        file_id = message.photo[-1].file_id
        file_unique_id = message.photo[-1].file_unique_id
        dialog_manager.dialog_data.setdefault("media_content", []).append(
            (file_id, file_unique_id),
        )
        msg_id = dialog_manager.dialog_data["message_id"]
        chat_id = dialog_manager.dialog_data["chat_id"]
        post_message = dialog_manager.dialog_data["post_message"]
        keyboard = dialog_manager.dialog_data.get("keyboard")
        await message.bot.edit_message_media(
            media=InputMediaPhoto(media=file_id, caption=post_message),
            chat_id=chat_id,
            message_id=msg_id,
            reply_markup=keyboard,
        )
        await message.bot.delete_messages(
            chat_id=chat_id, message_ids=[message.message_id - 1, message.message_id]
        )
        logger.debug(
            "Медиа успешно добавлено",
            extra={
                "user_id": message.from_user.id,
                "message_id": msg_id,
                "media_type": message.content_type,
            },
        )
        dialog_manager.dialog_data["has_media"] = True
        dialog_manager.dialog_data["type_media"] = message.content_type
    except Exception as e:
        logger.error(
            "Ошибка при добавлении медиа",
            extra={
                "user_id": message.from_user.id,
                "error": str(e),
                "error_type": type(e).__name__,
            },
            exc_info=True,
        )
        raise
    await dialog_manager.switch_to(state=PostingSG.creating_post)


async def process_invalid_media_content(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    """
    Обработка некорректных сообщений, если они не попадают под тайп видео, фото, кружка, гифки
    """
    i18n: TranslatorRunner = dialog_manager.middleware_data["i18n"]
    # dialog_manager.show_mode = ShowMode.DELETE_AND_SEND # пока оставим для экспериментов
    await message.answer(i18n.cr.instruction.media.invalid.type())


# Удаление медиа
async def process_remove_media(
    message: Message, widget: Button, dialog_manager: DialogManager
) -> None:
    """Удаляет медиа контент из сообщения"""
    msg_id = dialog_manager.dialog_data["message_id"]
    chat_id = dialog_manager.dialog_data["chat_id"]
    keyboard = dialog_manager.dialog_data.get("keyboard")
    post_message = dialog_manager.dialog_data["post_message"]

    await message.bot.delete_message(
        chat_id=chat_id,
        message_id=msg_id,
    )
    # Заново складываем в диалог дату обновленные данные
    new_message = await message.bot.send_message(
        chat_id=chat_id, text=post_message, reply_markup=keyboard
    )
    dialog_manager.dialog_data["message_id"] = new_message.message_id
    dialog_manager.dialog_data["has_media"] = False
    dialog_manager.dialog_data["media_content"] = None


# Настройка уведомлений
async def process_toggle_notify(
    message: Message, widget: Toggle, dialog_manager: DialogManager, state: str
):
    dialog_manager.dialog_data["notify_on"] = True if state == "turn_on" else False
    logger.info(
        f"\nПользователь: {message.from_user.first_name} [{message.from_user.username}] переключил настройку уведомлений\n"
        f"Текущее состояние поста: {state}\n"
    )


# Отправка прямо сейчас
async def process_push_now_to_channel_button(
    message: Message, widget: Button, dialog_manager: DialogManager
):
    """Отправка в Телеграм канал"""
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")
    keyboard = dialog_manager.dialog_data.get("keyboard")
    post_message = dialog_manager.dialog_data.get("post_message")
    notify_on = dialog_manager.dialog_data.get("notify_on")
    file_id = dialog_manager.dialog_data.get("media_content")
    multiselect: Multiselect = dialog_manager.find("selected_channel_for_publication")
    channels: list[str] = multiselect.get_checked()

    logger.info(
        "Начата отправка сообщения в каналы",
        extra={
            "user_id": message.from_user.id,
            "action": "push_to_channels",
            "channels_count": len(channels),
            "has_media": bool(dialog_manager.dialog_data.get("media_content")),
            "has_keyboard": bool(dialog_manager.dialog_data.get("keyboard")),
        },
    )

    if file_id is None:
        for channel_name in channels:
            channel_name = "@" + channel_name
            try:
                await message.bot.send_message(
                    chat_id=channel_name,
                    text=post_message,
                    reply_markup=keyboard,
                    disable_notification=notify_on,
                )
                logger.info(
                    "Сообщение отправлено в канал",
                    extra={
                        "user_id": message.from_user.id,
                        "channel": channel_name,
                        "status": "success",
                    },
                )
            except TelegramBadRequest as e:
                logger.error(
                    "Ошибка при отправке в канал",
                    extra={
                        "user_id": message.from_user.id,
                        "channel": channel_name,
                        "error": str(e),
                        "error_type": "TelegramBadRequest",
                    },
                )
                await message.answer(f"{i18n.error()}")
            finally:
                await dialog_manager.switch_to(state=PostingSG.show_posted_status)


async def process_push_now_to_bot_button(
    message: Message, widget: Button, dialog_manager: DialogManager
):
    """Моментальная отправка по пользователям бота"""
    session = dialog_manager.middleware_data.get("session")

    # получение списка ID пользователей
    telegram_ids = await get_all_customers(session=session)
    dialog_manager.dialog_data["count_acc_to_send"] = len(telegram_ids)

    # Пользовательские данные для сообщения
    keyboard = dialog_manager.dialog_data.get("keyboard")
    post_message = dialog_manager.dialog_data.get("post_message")
    file_id = dialog_manager.dialog_data.get("media_content")
    has_spoiler = dialog_manager.dialog_data.get("has_spoiler")
    notify_status = dialog_manager.dialog_data.get("notify_on")

    for telegram_id in telegram_ids:
        await send_message_bot_subscribers.kiq(
            chat_id=telegram_id,
            text=post_message,
            keyboard=keyboard,
            file_id=file_id,
            notify_status=notify_status,
            has_spoiler=has_spoiler,
        )
    logger.info(f"Запланировано к отправке {len(telegram_ids)} сообщений")
    await dialog_manager.switch_to(
        state=PostingSG.show_sended_status, show_mode=ShowMode.DELETE_AND_SEND
    )


async def process_push_to_bot_button(
    message: Message, widget: Button, dialog_manager: DialogManager
):
    """Отправка среди подписчиков бота"""
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")
    nats_source = dialog_manager.middleware_data.get("nats_source")
    session = dialog_manager.middleware_data.get("session")

    # получение списка ID пользователей
    telegram_ids = await get_all_customers(session=session)
    dialog_manager.dialog_data["count_acc_to_send"] = len(telegram_ids)
    timezone_label, tz_offset = await get_user_tz(
        session=session, telegram_id=message.from_user.id
    )

    # Пользовательские данные со временем
    tzinfo = timezone(timedelta(hours=tz_offset))
    posting_time_iso: str = dialog_manager.dialog_data.get(
        "dt_posting_iso", datetime.now(tz=tzinfo).isoformat()
    )
    posting_time = datetime.fromisoformat(posting_time_iso)

    # Пользовательские данные для сообщения
    keyboard = dialog_manager.dialog_data.get("keyboard")
    post_message = dialog_manager.dialog_data.get("post_message")
    notify_status = dialog_manager.dialog_data.get("notify_on")
    file_id = dialog_manager.dialog_data.get("media_content")
    type_media = dialog_manager.dialog_data.get("type_media")
    has_spoiler = dialog_manager.dialog_data.get("has_spoiler")
    recipient_type = dialog_manager.dialog_data.get("recipient_type")

    for telegram_id in telegram_ids:
        task = await send_schedule_message_bot_subscribers.schedule_by_time(
            source=nats_source,
            time=posting_time,
            chat_id=telegram_id,
            text=post_message,
            keyboard=keyboard,
            file_id=file_id,
            type_media=type_media,
            notify_status=notify_status,
            has_spoiler=has_spoiler,
        )
    await upsert_post(
        session=session,
        schedule_id=task.schedule_id,
        target_type=recipient_type,
        data_json={},
        post_message=post_message,
        author_id=message.from_user.id,
    )
    await dialog_manager.switch_to(
        state=PostingSG.show_sended_status, show_mode=ShowMode.DELETE_AND_SEND
    )


# Отправка по расписанию
async def process_send_to_channel_later(
    message: Message,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    nats_source = dialog_manager.middleware_data.get("nats_source")
    session = dialog_manager.middleware_data.get("session")

    # Предварительная подготовка
    timezone_label, tz_offset = await get_user_tz(
        session=session, telegram_id=message.from_user.id
    )

    # Пользовательские данные со временем
    posting_time_iso: str = dialog_manager.dialog_data["dt_posting_iso"]
    posting_time = datetime.fromisoformat(posting_time_iso).replace(
        tzinfo=timezone(timedelta(hours=tz_offset))
    )
    delay = int(get_delay(post_time=posting_time))

    # Пользовательские данные для сообщения
    selected_channels = dialog_manager.dialog_data["selected_channels"]
    post_message = dialog_manager.dialog_data.get("post_message")
    keyboard = dialog_manager.dialog_data.get("keyboard")
    notify_status = dialog_manager.dialog_data.get("notify_on")
    has_spoiler = dialog_manager.dialog_data.get("has_spoiler")
    file_id = dialog_manager.dialog_data.get("media_content")

    for channel in selected_channels:
        channel_name = "@" + channel[0]  # channel — это кортеж
        await send_message_to_channel.schedule_by_time(
            source=nats_source,
            time=posting_time,
            chat_id=channel_name,
            text=post_message,
            keyboard=keyboard,
            file_id=file_id,
            notify_status=notify_status,
            has_spoiler=has_spoiler,
        )
    await dialog_manager.switch_to(
        state=PostingSG.show_posted_status, show_mode=ShowMode.DELETE_AND_SEND
    )
