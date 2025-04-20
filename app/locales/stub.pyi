from typing import Literal

class TranslatorRunner:
    def get(self, path: str, **kwargs) -> str: ...

    start: Start
    cr: Cr
    channel: Channel
    settings: Settings

    @staticmethod
    def next() -> Literal["""⏭ Далее"""]: ...
    @staticmethod
    def cancel() -> Literal["""❌Отмена"""]: ...
    @staticmethod
    def back() -> Literal["""🔙 Назад"""]: ...
    @staticmethod
    def error() -> Literal["""⚠ Произошла ошибка"""]: ...
    @staticmethod
    def yes() -> Literal["""✔ Да"""]: ...
    @staticmethod
    def no() -> Literal["""Нет"""]: ...
    @staticmethod
    def edit() -> Literal["""✍ Изменить"""]: ...
    @staticmethod
    def delete() -> Literal["""🧹 Удалить"""]: ...
    @staticmethod
    def add() -> Literal["""➕ Добавить"""]: ...
    @staticmethod
    def caption() -> Literal[
        """Опубликовано через &lt;a href=&#34;https://sale-keeper.ru&#34;&gt;&lt;b&gt;💵Sale Keeper&lt;/b&gt;&lt;/a&gt;"""
    ]: ...

class Start:
    hello: StartHello
    create: StartCreate
    edit: StartEdit
    add: StartAdd

    @staticmethod
    def settings() -> Literal["""Настройки"""]: ...

class StartHello:
    @staticmethod
    def admin(
        *, username
    ) -> Literal[
        """Привет, { $username }👋

Я могу:
✍Составить описание товара✍
📅Запланировать пост📅
✍Подготовить карточку товара✍

✨Для демонстрации возможностей нажми /demo ✨"""
    ]: ...

class StartCreate:
    @staticmethod
    def post() -> Literal["""Создать пост"""]: ...
    @staticmethod
    def description() -> Literal["""Создать описание"""]: ...

class StartEdit:
    @staticmethod
    def post() -> Literal["""Редактировать пост"""]: ...

class StartAdd:
    @staticmethod
    def channel() -> Literal["""Мои каналы"""]: ...

class Cr:
    select: CrSelect
    watch: CrWatch
    invalid: CrInvalid
    reply: CrReply
    edit: CrEdit
    url: CrUrl
    set: CrSet
    unset: CrUnset
    add: CrAdd
    remove: CrRemove
    push: CrPush
    instruction: CrInstruction
    approve: CrApprove
    success: CrSuccess

class CrSelect:
    channel: CrSelectChannel
    bot: CrSelectBot
    channels: CrSelectChannels

class CrSelectChannel:
    to: CrSelectChannelTo

class CrSelectChannelTo:
    send: CrSelectChannelToSend

class CrSelectChannelToSend:
    @staticmethod
    def message() -> Literal[
        """Выберите место публикации вашего поста. 

&lt;i&gt;Общая рассылка — это рассылка сообщения по пользователям бота&lt;/i&gt;"""
    ]: ...

class CrSelectBot:
    to: CrSelectBotTo

class CrSelectBotTo:
    send: CrSelectBotToSend

class CrSelectBotToSend:
    @staticmethod
    def message() -> Literal["""🤖 Общая рассылка"""]: ...

class CrWatch:
    @staticmethod
    def text() -> Literal[
        """✍ Отправьте текст поста, который необходимо опубликовать"""
    ]: ...

class CrInvalid:
    @staticmethod
    def data() -> Literal[
        """❌ Не поддерживаю такой тип данных ❌  

Для демонстрации бота нажмите /demo или напишите в поддержку бота"""
    ]: ...

class CrReply:
    @staticmethod
    def text() -> Literal["""👆 Проверьте текст, перед публикацей"""]: ...

class CrEdit:
    @staticmethod
    def text() -> Literal["""✍Изменить текст"""]: ...

class CrUrl:
    @staticmethod
    def btns() -> Literal["""☑️URL Кнопки"""]: ...
    @staticmethod
    def delete() -> Literal["""❌ Удалить кнопки"""]: ...

class CrSet:
    @staticmethod
    def time() -> Literal["""🕙Время отправки"""]: ...
    @staticmethod
    def notify() -> Literal["""🔔С уведомлением"""]: ...

class CrUnset:
    @staticmethod
    def notify() -> Literal["""🔕Без уведомления"""]: ...
    @staticmethod
    def comments() -> Literal["""☑️Отключить комментарии"""]: ...

class CrAdd:
    @staticmethod
    def media() -> Literal["""➕Добавить медиа"""]: ...

class CrRemove:
    @staticmethod
    def media() -> Literal["""❌Удалить медиа"""]: ...

class CrPush:
    later: CrPushLater

    @staticmethod
    def now() -> Literal["""🚀Отправить сейчас"""]: ...

class CrPushLater:
    button: CrPushLaterButton

    @staticmethod
    def __call__() -> Literal["""📅Запланировать пост"""]: ...
    @staticmethod
    def message(
        *, current_date
    ) -> Literal[
        """Планирование поста на &lt;b&gt; { $current_date } &lt;/b&gt;

Нажмите &lt;b&gt;Планировать 📌&lt;/b&gt;, чтобы подтвердить и запланировать пост в каналы:"""
    ]: ...

class CrInstruction:
    delayed: CrInstructionDelayed
    invalid: CrInstructionInvalid
    media: CrInstructionMedia

    @staticmethod
    def url() -> Literal[
        """⚠ Отправьте кнопки в формате:
Link - https://ya.ru | Link 2 - https://no.com
Link 3 - http://ac.ru | Link 4 - http://mail.ru

Каждую новую кнопку отправьте с новой строки.
Если хотите разместить несколько кнопок в одной строке используйте разделитель « | »"""
    ]: ...

class CrInstructionDelayed:
    @staticmethod
    def post(
        *, tz
    ) -> Literal[
        """&lt;b&gt;Отправьте время выхода поста в часовом поясе { $tz } в любом удобном формате, например:&lt;/b&gt;
&lt;blockquote&gt;
18 - текущие сутки 18:00
0830 - текущие сутки 08:30
08 30 - текущие сутки 08:30
1830 - текущие сутки 18:30
18300408 - 18:30 04.08
18 30 04 08 - 18:30 04.08
&lt;/blockquote&gt;"""
    ]: ...

class CrInstructionInvalid:
    @staticmethod
    def time(
        *, tz
    ) -> Literal[
        """Не поддерживаю такой формат ввода данных 🤷‍♂️
&lt;b&gt;Отправьте время выхода поста в часовом поясе { $tz } в любом удобном формате, например:&lt;/b&gt;
&lt;blockquote&gt;
18 - текущие сутки 18:00
0830 - текущие сутки 08:30
08 30 - текущие сутки 08:30
1830 - текущие сутки 18:30
18300408 - 18:30 04.08
18 30 04 08 - 18:30 04.08
&lt;/blockquote&gt;"""
    ]: ...

class CrInstructionMedia:
    invalid: CrInstructionMediaInvalid

    @staticmethod
    def post() -> Literal["""📷 Пришлите медиа файлы"""]: ...
    @staticmethod
    def approve() -> Literal["""Все медиа файлы отправлены ❓"""]: ...
    @staticmethod
    def yes() -> Literal["""✅ Да"""]: ...
    @staticmethod
    def no() -> Literal["""❌ Нет"""]: ...

class CrInstructionMediaInvalid:
    @staticmethod
    def type() -> Literal[
        """❌ Не поддерживаю такой тип данных ❌  
Допустимые форматы:
- Фото
- Видео

Для демонстрации бота нажмите /demo или напишите в &lt;a href=&#34;@inactive0073&#34;&gt;поддержку бота&lt;/a&gt;"""
    ]: ...

class CrSelectChannels:
    to: CrSelectChannelsTo

class CrSelectChannelsTo:
    push: CrSelectChannelsToPush

class CrSelectChannelsToPush:
    @staticmethod
    def message() -> Literal["""Выберите каналы для публикации поста."""]: ...

class CrApprove:
    media: CrApproveMedia

class CrApproveMedia:
    push: CrApproveMediaPush

class CrApproveMediaPush:
    @staticmethod
    def now() -> Literal["""Отправить сейчас?"""]: ...

class CrPushLaterButton:
    @staticmethod
    def caption() -> Literal["""Планировать 📌"""]: ...

class CrSuccess:
    @staticmethod
    def pushed(
        *, post_message, date_posting
    ) -> Literal[
        """Пост &#34;{ $post_message }&#34;
успешно опубликован в &lt;b&gt;{ $date_posting }&lt;/b&gt;
в каналах:"""
    ]: ...

class Channel:
    add: ChannelAdd
    _not: Channel_not
    instruction: ChannelInstruction
    link: ChannelLink
    settings: ChannelSettings
    delete: ChannelDelete
    success: ChannelSuccess
    unsuccessful: ChannelUnsuccessful
    caption: ChannelCaption

    @staticmethod
    def exists() -> Literal["""Ниже представлен список ваших каналов."""]: ...

class ChannelAdd:
    channel: ChannelAddChannel

    @staticmethod
    def caption() -> Literal["""✍ Добавить автоподпись"""]: ...

class ChannelAddChannel:
    @staticmethod
    def button() -> Literal["""Добавить канал"""]: ...

class Channel_not:
    @staticmethod
    def exists() -> Literal["""У вас не добавлен ни один канал."""]: ...

class ChannelInstruction:
    @staticmethod
    def add() -> Literal[
        """Для добавления бота сделайте бота администратором в канале и дайте ему права на управление сообщениями и управление историями. 
После добавления бота отправьте ссылку на канал в формате &lt;b&gt;@channelusername&lt;/b&gt;"""
    ]: ...

class ChannelLink:
    wrong: ChannelLinkWrong
    after: ChannelLinkAfter

    @staticmethod
    def addition() -> Literal[
        """https://t.me/saler_scheduler_bot?startchannel&amp;admin=post_messages+edit_messages+delete_messages+invite_users"""
    ]: ...
    @staticmethod
    def invalid() -> Literal[
        """Что-то не так с ссылкой на канал, проверьте её и отправьте в формате &lt;b&gt;@channelusername&lt;/b&gt;"""
    ]: ...

class ChannelLinkWrong:
    @staticmethod
    def type() -> Literal[
        """🤖 Бот может работать только с каналами. 
Типы приватных чатов, групп и форумов не поддерживаются."""
    ]: ...

class ChannelLinkAfter:
    joining: ChannelLinkAfterJoining

class ChannelLinkAfterJoining:
    @staticmethod
    def channel() -> Literal[
        """🙌 Бот успешно добавлен в администраторы канала."""
    ]: ...

class ChannelSettings:
    @staticmethod
    def desc(
        *, channel_name, caption
    ) -> Literal[
        """🛠 Настройки канала &lt;b&gt;{ $channel_name }&lt;/b&gt;

Подпись: { $caption }"""
    ]: ...

class ChannelDelete:
    _from: ChannelDelete_from
    channel: ChannelDeleteChannel

    @staticmethod
    def button() -> Literal["""Удалить бота 🤖"""]: ...

class ChannelDelete_from:
    @staticmethod
    def bot() -> Literal["""❌ Удалить канал из телеграм бота"""]: ...

class ChannelDeleteChannel:
    @staticmethod
    def instruction() -> Literal[
        """⚠ Вы удаляете бота из канала ⚠

Если вы уверены нажмите &lt;b&gt;Удалить бота 🤖&lt;/b&gt;"""
    ]: ...

class ChannelSuccess:
    @staticmethod
    def deleted() -> Literal["""Бот успешно удален"""]: ...

class ChannelUnsuccessful:
    @staticmethod
    def deleted() -> Literal[
        """Бот не был удален, попробуйте повторить попытку позже. 

Если проблема повторяется - напишите в техническую поддержку 💻."""
    ]: ...

class ChannelCaption:
    _not: ChannelCaption_not

    @staticmethod
    def on() -> Literal["""✔ Автоподпись включена"""]: ...
    @staticmethod
    def off() -> Literal["""❌ Автоподпись выключена"""]: ...
    @staticmethod
    def error() -> Literal[
        """📝В качестве подписи к тексту принимается только текст."""
    ]: ...
    @staticmethod
    def wait() -> Literal["""Пришлите новую подпись к постам"""]: ...

class ChannelCaption_not:
    @staticmethod
    def exists() -> Literal["""У этого канала на данный момент нет автоподписи"""]: ...

class Settings:
    main: SettingsMain
    timezone: SettingsTimezone
    support: SettingsSupport
    select: SettingsSelect

class SettingsMain:
    @staticmethod
    def menu() -> Literal[
        """&lt;b&gt;Настройки&lt;/b&gt;

Настройте конфигурацию вашего бота."""
    ]: ...

class SettingsTimezone:
    @staticmethod
    def button() -> Literal["""🌍 Часовой пояс"""]: ...

class SettingsSupport:
    @staticmethod
    def button() -> Literal["""🤝 Онлайн-поддержка"""]: ...
    @staticmethod
    def message() -> Literal[
        """Для вопросов и предложений открыт: &lt;a href=&#34;@inactive0073&#34;&gt;@inactive0073&lt;/a&gt;

Всегда открыты и заинтересованы в решении ваших задач!"""
    ]: ...

class SettingsSelect:
    @staticmethod
    def timezone(
        *, current_timezone, local_datetime
    ) -> Literal[
        """Выберете ваш часовой пояс.

Ваш выбранный часовой пояс: &lt;b&gt;{ $current_timezone }&lt;/b&gt;.
Локальное время: &lt;b&gt;{ $local_datetime }&lt;/b&gt;"""
    ]: ...
