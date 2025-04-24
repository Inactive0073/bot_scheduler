from typing import TYPE_CHECKING

from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    CallbackQuery,
    InputMediaPhoto,
    InputMediaVideo,
)
from aiogram.exceptions import TelegramBadRequest

from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import Button, Toggle, Multiselect, ManagedMultiselect

from app.db.customer_requests import get_all_customers
from app.db.requests import get_user_tz
from app.dialogs.creating_post.services import get_delay
from app.states.creating_post import PostingSG

from datetime import datetime, timezone, timedelta

from logging import getLogger

from nats.js.client import JetStreamContext

from app.services.delay_service.publisher import delay_message_sending

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner  # type: ignore

logger = getLogger(__name__)


async def process_to_select_bot_mailing(
    message: Message, widget: Button, dialog_manager: DialogManager
) -> None:
    """Сеттер для типа получателя бот"""
    dialog_manager.dialog_data["recipient_type"] = "bot"


async def process_to_select_channel(
    message: Message, widget: ManagedMultiselect, dialog_manager: DialogManager, data
) -> None:
    """Сеттер для типа получателя канал"""
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
        f"Пользователь {message.from_user.username}|{message.from_user.id} создает новый пост"
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
        logger.debug(f"Пост успешно сохранен в dialog_data: {copy_msg.text[:50]}...")
    except Exception as e:
        logger.critical(
            f"Ошибка при создании поста пользователем {message.from_user.username}: {str(e)}"
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
        f"Пользователь {message.from_user.username} добавляет URL-кнопки к посту"
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
            f"Кнопки успешно добавлены к посту. Keyboard data: {keyboard.model_dump()}"
        )
    except Exception as e:
        logger.critical(f"Ошибка при добавлении кнопок к посту: {str(e)}")
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
    logger.info(f"Пользователь {message.from_user.username} добавляет медиа к посту")
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
        logger.debug(f"Медиа успешно добавлено к посту. File ID: {file_id[:15]}...")
        dialog_manager.dialog_data["has_media"] = True
    except Exception as e:
        logger.critical(f"Ошибка при добавлении медиа к посту: {str(e)}")
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
    chat_id = dialog_manager.dialog_data.get("chat_id")
    keyboard = dialog_manager.dialog_data.get("keyboard")
    post_message = dialog_manager.dialog_data.get("post_message")
    notify_on = dialog_manager.dialog_data.get("notify_on")
    file_id = dialog_manager.dialog_data.get("media_content")
    multiselect: Multiselect = dialog_manager.find("selected_channel_for_publication")
    channels: list[str] = multiselect.get_checked()

    logger.info(f"Полученные данные:{chat_id=}, {post_message=}, {notify_on=}")

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
                logger.info(f"Сообщение отправлено в канал: {channel_name}")
            except TelegramBadRequest as e:
                logger.info(
                    f"Ошибка во время выполнения рассылки в {channel_name}.\n{e!r}"
                )
                await message.answer(f"{i18n.error()}")
            finally:
                await dialog_manager.switch_to(state=PostingSG.show_posted_status)


async def process_push_now_to_bot_button(
    message: Message, widget: Button, dialog_manager: DialogManager
):
    """Моментальная отправка по пользователям бота"""
    js: JetStreamContext = dialog_manager.middleware_data.get("js")
    delay_send_subject: str = dialog_manager.middleware_data.get(
        "delay_send_subject_subscriber"
    )
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")


async def process_push_to_bot_button(
    message: Message, widget: Button, dialog_manager: DialogManager
):
    """Отправка среди подписчиков бота"""
    js: JetStreamContext = dialog_manager.middleware_data.get("js")
    delay_send_subject: str = dialog_manager.middleware_data.get(
        "delay_send_subject_subscriber"
    )
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")
    session = dialog_manager.middleware_data.get("session")

    # получение списка ID пользователей
    telegram_ids = await get_all_customers(session=session)
    timezone_label, tz_offset = await get_user_tz(
        session=session, telegram_id=message.from_user.id
    )

    # Пользовательские данные со временем
    tzinfo = timezone(timedelta(hours=tz_offset))
    posting_time_iso: str = dialog_manager.dialog_data.get(
        "dt_posting_iso", datetime.now(tz=tzinfo).isoformat()
    )
    posting_time = datetime.fromisoformat(posting_time_iso)
    delay = int(get_delay(post_time=posting_time))

    # Пользовательские данные для сообщения
    keyboard = dialog_manager.dialog_data.get("keyboard")
    post_message = dialog_manager.dialog_data.get("post_message")
    notify_on = dialog_manager.dialog_data.get("notify_on")
    file_id = dialog_manager.dialog_data.get("media_content")
    has_spoiler = dialog_manager.dialog_data.get("has_spoiler")

    for telegram_id in telegram_ids:
        await delay_message_sending(
            js=js,
            chat_id=telegram_id,
            text=post_message,
            subject=delay_send_subject,
            delay=delay,
            tz_label=timezone_label,
            tz_offset=tz_offset,
            keyboard=keyboard,
            file_id=file_id,
            notify_status=notify_on,
            has_spoiler=has_spoiler,
        )


# Отправка по расписанию
async def process_send_to_channel_later(
    message: Message,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    js: JetStreamContext = dialog_manager.middleware_data.get("js")
    delay_send_subject: str = dialog_manager.middleware_data.get(
        "delay_send_subject_channel"
    )
    session = dialog_manager.middleware_data.get("session")

    # Предварительная подготовка
    timezone_label, tz_offset = await get_user_tz(
        session=session, telegram_id=message.from_user.id
    )

    # Пользовательские данные со временем
    posting_time_iso: str = dialog_manager.dialog_data["dt_posting_iso"]
    posting_time = datetime.fromisoformat(posting_time_iso)
    posting_time.replace(tzinfo=timezone(timedelta(hours=tz_offset)))
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
        await delay_message_sending(
            js=js,
            chat_id=channel_name,
            text=post_message,
            subject=delay_send_subject,
            delay=delay,
            tz_label=timezone_label,
            tz_offset=tz_offset,
            keyboard=keyboard,
            file_id=file_id,
            notify_status=notify_status,
            has_spoiler=has_spoiler,
        )
    await dialog_manager.switch_to(
        state=PostingSG.show_posted_status, show_mode=ShowMode.DELETE_AND_SEND
    )
