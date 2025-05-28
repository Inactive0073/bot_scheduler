from typing import Literal

class TranslatorRunner:
    def get(self, path: str, **kwargs) -> str: ...

    a: A
    customer: Customer
    waiter: Waiter
    start: Start
    cr: Cr
    channel: Channel
    settings: Settings
    admin: Admin

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
        """Сделано через &lt;a href=&#34;https://sale-keeper.ru&#34;&gt;&lt;b&gt;💵Sale Keeper&lt;/b&gt;&lt;/a&gt;"""
    ]: ...

class A:
    u: AU

class AU:
    @staticmethod
    def sure() -> Literal["""Вы уверены?"""]: ...

class Customer:
    hello: CustomerHello
    meeting: CustomerMeeting
    error: CustomerError
    menu: CustomerMenu
    balance: CustomerBalance
    no: CustomerNo
    card: CustomerCard
    catalog: CustomerCatalog
    delivery: CustomerDelivery
    loyalty: CustomerLoyalty
    partnership: CustomerPartnership
    about: CustomerAbout
    support: CustomerSupport

class CustomerHello:
    @staticmethod
    def message() -> Literal[
        """Добро пожаловать в чат-бот программы лояльности «Других ресторанов»! 😊

Поделитесь, пожалуйста, Вашим номером телефона. Просто нажмите на кнопку «Отправить контакт».👇

Поделившись своим номером, вы подтверждаете свое согласие с политикой конфиденциальности и офертой программы лояльности. 👉&lt;a href=&#34;https://ya.ru&#34;&gt;Тут подробно&lt;/a&gt;:"""
    ]: ...

class CustomerMeeting:
    gender: CustomerMeetingGender

    @staticmethod
    def phone() -> Literal["""Отправить контакт"""]: ...
    @staticmethod
    def name() -> Literal["""Отлично, теперь введите Ваше имя"""]: ...
    @staticmethod
    def surname() -> Literal[
        """Продолжим наше знакомство? 😉
Введите свою фамилию, чтобы мы могли начать заполнять Вашу анкету."""
    ]: ...
    @staticmethod
    def email() -> Literal[
        """Еще нам понадобится Ваш e-mail 💌
Иногда будем отправлять Вам полезную информацию на почту об акциях, скидках и сезонных предложениях."""
    ]: ...
    @staticmethod
    def birthday() -> Literal[
        """Укажите Вашу дату рождения в формате дд.мм.гггг. А мы порадуем Вас подарком.🎁"""
    ]: ...
    @staticmethod
    def thanks() -> Literal["""Отлично! Спасибо❤️"""]: ...

class CustomerError:
    @staticmethod
    def phone() -> Literal[
        """Отправленный номер не соответствует вашему номеру с аккаунта которого вы пишите. Нажмите на кнопку &lt;b&gt;Отправить контакт&lt;/b&gt;"""
    ]: ...
    @staticmethod
    def name() -> Literal[
        """Не смог обработать Ваше сообщение. Введите Ваше имя"""
    ]: ...
    @staticmethod
    def surname() -> Literal[
        """Не смог обработать Ваше сообщение. Введите Вашу фамилию"""
    ]: ...
    @staticmethod
    def birthday() -> Literal[
        """Не удалось записать Ваш день рождения. Введите его в формате &lt;b&gt;дд.мм.гггг&lt;/b&gt;"""
    ]: ...

class CustomerMeetingGender:
    @staticmethod
    def __call__() -> Literal[
        """🤩 Здорово! Осталось совсем чуть-чуть — укажите Ваш пол."""
    ]: ...
    @staticmethod
    def m() -> Literal["""Мужской"""]: ...
    @staticmethod
    def f() -> Literal["""Женский"""]: ...

class CustomerMenu:
    info: CustomerMenuInfo
    balance: CustomerMenuBalance
    about: CustomerMenuAbout
    card: CustomerMenuCard
    gifts: CustomerMenuGifts
    delivery: CustomerMenuDelivery
    loyalty: CustomerMenuLoyalty
    partnership: CustomerMenuPartnership
    help: CustomerMenuHelp

    @staticmethod
    def placeholder() -> Literal["""Выберите пункт меню"""]: ...

class CustomerMenuInfo:
    @staticmethod
    def message() -> Literal[
        """Нажмите на интересующие вас разделы в главном меню чат-бота. 
Тут все просто! 
Жмите на иконку 🎛 в правом нижнем углу."""
    ]: ...

class CustomerMenuBalance:
    @staticmethod
    def button() -> Literal["""Баланс и уровень"""]: ...

class CustomerMenuAbout:
    @staticmethod
    def button() -> Literal["""Наши заведения ❤️"""]: ...

class CustomerMenuCard:
    @staticmethod
    def button() -> Literal["""Показать карту"""]: ...

class CustomerMenuGifts:
    @staticmethod
    def button() -> Literal["""Каталог подарков"""]: ...

class CustomerMenuDelivery:
    @staticmethod
    def button() -> Literal["""Доставка"""]: ...

class CustomerMenuLoyalty:
    @staticmethod
    def button() -> Literal["""Правила программы лояльности"""]: ...

class CustomerMenuPartnership:
    @staticmethod
    def button() -> Literal["""Сотрудничество"""]: ...

class CustomerMenuHelp:
    @staticmethod
    def button() -> Literal["""Помощь"""]: ...

class CustomerBalance:
    @staticmethod
    def message(
        *, current_balance, date_expire, balance_to_expire, visits, percent_cashback
    ) -> Literal[
        """Ваша бонусная информация


&lt;b&gt;Баланс бонусов:&lt;/b&gt; { $current_balance }
&lt;b&gt;Ближайшая дата сгорания бонусов:&lt;/b&gt; { $date_expire }
&lt;b&gt;Количество бонусов к сгоранию:&lt;/b&gt; { $balance_to_expire }
&lt;b&gt;Количество визитов:&lt;/b&gt; { $visits }
&lt;b&gt;Процент кэшбэка:&lt;/b&gt; { $percent_cashback }


Если вам недоступны бонусы и карта, поделитесь с нами своим номером телефона, вызвав команду /start"""
    ]: ...

class CustomerNo:
    balance: CustomerNoBalance

class CustomerNoBalance:
    @staticmethod
    def message() -> Literal["""На данный момент ваш баланс 0 бонусов."""]: ...

class CustomerCard:
    @staticmethod
    def message(
        *, number_card
    ) -> Literal["""Номер вашей карты: &lt;b&gt;{ $number_card }&lt;/b&gt;"""]: ...

class CustomerCatalog:
    @staticmethod
    def message() -> Literal[
        """Чтобы приобрести товары из Каталога подарков вы можете: 
— Посетить свой любимый ресторан, сделать заказ с позицией из Каталога подарков и сообщить об этом официанту;
— Позвонить в свой любимый ресторан и зарезервировать товар из Каталога подарков;
— Написать нам в чат о том, что вы хотите забронировать позицию из Каталога подарков, назвать свой любимый ресторан и сообщить, когда вам будет удобно забрать подарок. Мы сообщим о вашем бронировании! 

Подарок можно будет забрать в зале заведений: «Другие рестораны», но скоро будет доступен самовывоз. Только тсс, никому не говорите!

Обратите внимание, что подарочные сертификаты, приобретенные за бонусы, не подлежат возврату или обмену на денежные средства. Подарочные сертификаты необходимо бронировать не менее чем за 3 дня до выдачи."""
    ]: ...
    @staticmethod
    def button() -> Literal["""Позвонить в ресторан"""]: ...
    @staticmethod
    def link() -> Literal["""https://drugierestorany.ru/kontakty"""]: ...

class CustomerDelivery:
    @staticmethod
    def message() -> Literal[
        """Вы можете заказать доставку от любимых заведений. Будьте внимательны, программа лояльности не действует за заказы на доставку и самовывоз."""
    ]: ...
    @staticmethod
    def button() -> Literal["""Заказать доставку в Другие рестораны"""]: ...
    @staticmethod
    def link() -> Literal["""https://antresol.drugierestorany.ru/dostavka"""]: ...

class CustomerLoyalty:
    @staticmethod
    def message() -> Literal[
        """Добро пожаловать в программу лояльности &#34;Другие рестораны&#34; 😎! 

Что даёт наша программа лояльности?

- Кэшбэк от 3% до 10% с каждой покупки
- Персональные предложения и акции — следите за уведомлениями в боте и не упускайте подарки и выгоду
- Доступ к каталогу подарков сразу после регистрации 
- Возможность оплаты бонусами до 20% от чека при достижении уровня 10%

Важная информация:
- Баллы начисляются с каждого чека
- В прогресс уровня учитывается сумма покупки от 400 р
- Уровень 10% нужно подтверждать — 20 визитов в течение 365 дней с момента достижения уровня 10%"""
    ]: ...
    @staticmethod
    def button() -> Literal["""Открыть каталог подарков"""]: ...
    @staticmethod
    def link() -> Literal["""https://gifts.drugierestorany.ru/"""]: ...

class CustomerPartnership:
    info: CustomerPartnershipInfo

class CustomerPartnershipInfo:
    @staticmethod
    def message() -> Literal[
        """Если Вы хотите стать нашим партнером, или у Вас есть предложения по другим видам сотрудничества с DrugieRestorany, пожалуйста, напишите нам по адресу &lt;a href=&#34;mailto:drugie@restorany.ru&#34;&gt;drugie@restorany.ru&lt;/a&gt;"""
    ]: ...

class CustomerAbout:
    info: CustomerAboutInfo
    message: CustomerAboutMessage
    link: CustomerAboutLink

class CustomerAboutInfo:
    @staticmethod
    def message() -> Literal[
        """Другие рестораны – большая семья современных ресторанов, где любят душевно встречать, шумно поздравлять, и, главное, вкусно кормить!"""
    ]: ...

class CustomerAboutMessage:
    @staticmethod
    def menu() -> Literal["""Посмотреть меню"""]: ...
    @staticmethod
    def take() -> Literal["""Забронировать"""]: ...
    @staticmethod
    def delivery() -> Literal["""Доставка &amp; Самовывоз"""]: ...
    @staticmethod
    def schedule() -> Literal["""Режим работы"""]: ...
    @staticmethod
    def route() -> Literal["""Как добраться"""]: ...
    @staticmethod
    def social() -> Literal["""Другие рестораны в социальных сетях"""]: ...

class CustomerAboutLink:
    @staticmethod
    def menu() -> Literal["""https://antresol.drugierestorany.ru/menu"""]: ...
    @staticmethod
    def take() -> Literal[
        """https://eda.yandex.ru/r/antresol?placeSlug=antresol_uonxj"""
    ]: ...
    @staticmethod
    def delivery() -> Literal[
        """https://eda.yandex.ru/r/antresol?placeSlug=antresol_uonxj"""
    ]: ...
    @staticmethod
    def schedule() -> Literal["""https://antresol.drugierestorany.ru/#adresa"""]: ...
    @staticmethod
    def route() -> Literal[
        """https://yandex.com/maps/195/ulyanovsk/chain/antresol_/105211848933/?ll=48.473725%2C54.338800&amp;sll=48.395548%2C54.319786&amp;source=serp_navig&amp;sspn=0.018024%2C0.007940&amp;utm_source=share&amp;z=12.22"""
    ]: ...
    @staticmethod
    def social() -> Literal["""https://vk.com/antresolfamily"""]: ...

class CustomerSupport:
    @staticmethod
    def message() -> Literal[
        """Свяжитесь с &lt;a href=&#34;@inactive0073&#34;&gt;нами&lt;/a&gt;, если у вас возникли трудности при использовании сервиса."""
    ]: ...

class Waiter:
    hello: WaiterHello
    menu: WaiterMenu
    success: WaiterSuccess
    invalid: WaiterInvalid
    processing: WaiterProcessing

class WaiterHello:
    @staticmethod
    def message() -> Literal[
        """Ваша роль: &lt;b&gt;Официант&lt;/b&gt;
Для получения инструкции по работе с ботом, нажмите &lt;a href=&#34;/instruction&#34;&gt;/instruction&lt;/a&gt;"""
    ]: ...

class WaiterMenu:
    @staticmethod
    def scan() -> Literal["""Сканировать"""]: ...

class WaiterSuccess:
    info: WaiterSuccessInfo

class WaiterSuccessInfo:
    @staticmethod
    def customer(
        *, name, balance, date_expire, bonus_to_expire
    ) -> Literal[
        """Данные по пользователю успешно получены. 
---  
👤 &lt;b&gt;Имя:&lt;/b&gt; { $name }  
💰 &lt;b&gt;Кол-во бонусов:&lt;/b&gt; { $balance }  
📅 &lt;b&gt;Бонусы сгорают:&lt;/b&gt; { $date_expire }  
🔥 &lt;b&gt;Количество бонусов к списанию:&lt;/b&gt; { $bonus_to_expire }  
---"""
    ]: ...

class WaiterInvalid:
    info: WaiterInvalidInfo

class WaiterInvalidInfo:
    @staticmethod
    def customer() -> Literal[
        """Нет данных по пользователю. 

Проверьте QR-Code или введите номер токена вручную."""
    ]: ...

class WaiterProcessing:
    add: WaiterProcessingAdd
    subtract: WaiterProcessingSubtract
    adding: WaiterProcessingAdding
    subtracting: WaiterProcessingSubtracting

    @staticmethod
    def instruction() -> Literal[
        """&lt;b&gt;РАБОТА С КЛИЕНТОМ&lt;/b&gt;

Для начисления: &lt;b&gt;➕Начисить бонусы&lt;/b&gt;
Для списания: &lt;b&gt;➖Списать бонусы&lt;/b&gt;
Для возврата: &lt;b&gt;🔙 Назад&lt;/b&gt;"""
    ]: ...

class WaiterProcessingAdd:
    @staticmethod
    def bonus() -> Literal["""➕Начислить бонусы"""]: ...

class WaiterProcessingSubtract:
    @staticmethod
    def bonus() -> Literal["""➖Списать бонусы"""]: ...

class WaiterProcessingAdding:
    bonus: WaiterProcessingAddingBonus

    @staticmethod
    def success(
        *, amount
    ) -> Literal[
        """Бонусы успешно начислены. 

&lt;b&gt;&lt;i&gt;Было начислено { $amount } б.&lt;/i&gt;&lt;/b&gt;"""
    ]: ...
    @staticmethod
    def unsuccess() -> Literal[
        """Не удалось начислить бонусы. Проверьте данные и попробуйте снова."""
    ]: ...

class WaiterProcessingAddingBonus:
    @staticmethod
    def instruction() -> Literal[
        """Введите сумму чека стола для начисления бонусов. 

Вводите именно итоговую сумму чека. Бонусы будут рассчитаны автоматически."""
    ]: ...

class WaiterProcessingSubtracting:
    not_: WaiterProcessingSubtractingNot_

    @staticmethod
    def instruction() -> Literal["""Укажите сумму бонусов для списания."""]: ...
    @staticmethod
    def success() -> Literal["""Бонусы успешно списаны."""]: ...
    @staticmethod
    def unsuccess() -> Literal[
        """Не удалось списать бонусы. Проверьте данные и попробуйте снова. 

Возможно, вы указали неверную сумму или у вас недостаточно бонусов. Для возврата в основное меню нажмите &lt;a href=&#34;/reset&#34;&gt;/reset&lt;/a&gt;"""
    ]: ...

class WaiterProcessingSubtractingNot_:
    @staticmethod
    def enough() -> Literal[
        """Введеное значение превышает доступное количество бонусов."""
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
    def admin() -> Literal[
        """Ваша роль: &lt;b&gt;Менеджер&lt;/b&gt;

Доступный функционал:

📅 Планирование поста
✍ Добавление каналов для рассылок
📤 Рассылка по пользователям бота
📤 Рассылка в каналы

Для получения инструкции нажми &lt;a href=&#34;/demo&#34;&gt;/demo&lt;/a&gt;
&lt;b&gt;&lt;i&gt;Важно!&lt;/i&gt;&lt;/b&gt;
Перед началом работы проверьте и укажите корректный часовой пояс в настройках"""
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
    send: CrSuccessSend

    @staticmethod
    def pushed(
        *, post_message, date_posting
    ) -> Literal[
        """Пост &#34;{ $post_message }&#34;
успешно запланирован на &lt;b&gt;{ $date_posting }&lt;/b&gt;
в каналах:"""
    ]: ...

class CrSuccessSend:
    bot: CrSuccessSendBot

class CrSuccessSendBot:
    @staticmethod
    def subscribers(
        *, post_message, date_posting, count_people, count_user
    ) -> Literal[
        """Рассылка с материалом &#34;{ $post_message }&#34;
успешно запланирована на &lt;b&gt;{ $date_posting }&lt;/b&gt;

Количество получателей: &lt;b&gt;{ $count_people }&lt;/b&gt; { $count_user -&gt;
[1] юзер
*[other] юзеров
}"""
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
        """Для вопросов и предложений: &lt;a href=&#34;@inactive0073&#34;&gt;@inactive0073&lt;/a&gt;

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

class Admin:
    not_: AdminNot_
    comeback: AdminComeback
    hello: AdminHello
    ban: AdminBan
    role: AdminRole
    reports: AdminReports
    team: AdminTeam

class AdminNot_:
    found: AdminNot_Found

class AdminNot_Found:
    @staticmethod
    def user() -> Literal[
        """Пользователь не найден. Проверьте данные и попробуйте еще раз.

Допустимый формат поиска: &lt;b&gt;123455&lt;/b&gt;, если ищем по Telegram ID или &lt;b&gt;@username&lt;/b&gt;, если ищем по имени пользователя."""
    ]: ...

class AdminComeback:
    @staticmethod
    def btn() -> Literal["""🔙 В админ меню"""]: ...

class AdminHello:
    @staticmethod
    def message() -> Literal[
        """Ваша роль: &lt;b&gt;Администратор&lt;/b&gt;

Доступный функционал:

📱 Функционал менеджера
👨‍💼 Управление командой
📃 Отчет системы лояльности персонала"""
    ]: ...

class AdminBan:
    menu: AdminBanMenu
    not_: AdminBanNot_
    success: AdminBanSuccess
    unban: AdminBanUnban

    @staticmethod
    def ban() -> Literal["""Заблокировать"""]: ...

class AdminBanMenu:
    @staticmethod
    def btn() -> Literal["""Блокировка/разблокировка"""]: ...
    @staticmethod
    def msg() -> Literal[
        """Напишите &lt;b&gt;ID телеграм&lt;/b&gt; пользователя или &lt;b&gt;@username&lt;/b&gt;."""
    ]: ...

class AdminRole:
    customer: AdminRoleCustomer
    waiter: AdminRoleWaiter
    manager: AdminRoleManager

class AdminRoleCustomer:
    @staticmethod
    def btn() -> Literal["""Клиент"""]: ...

class AdminRoleWaiter:
    @staticmethod
    def btn() -> Literal["""Официант"""]: ...

class AdminRoleManager:
    @staticmethod
    def btn() -> Literal["""Менеджер"""]: ...

class AdminReports:
    menu: AdminReportsMenu
    all_: AdminReportsAll_
    bonus: AdminReportsBonus

    @staticmethod
    def btn() -> Literal["""Отчеты"""]: ...

class AdminTeam:
    menu: AdminTeamMenu
    invite: AdminTeamInvite
    select: AdminTeamSelect
    already: AdminTeamAlready
    kick: AdminTeamKick
    approve: AdminTeamApprove

    @staticmethod
    def btn() -> Literal["""Команда"""]: ...

class AdminReportsMenu:
    @staticmethod
    def msg() -> Literal["""Выберите отчет для просмотра"""]: ...

class AdminReportsAll_:
    users: AdminReportsAll_Users
    scheduled_posts: AdminReportsAll_Scheduled_posts

class AdminReportsAll_Users:
    @staticmethod
    def btn() -> Literal["""Выгрузить клиентов"""]: ...

class AdminReportsBonus:
    accrual: AdminReportsBonusAccrual

class AdminReportsBonusAccrual:
    records: AdminReportsBonusAccrualRecords

class AdminReportsBonusAccrualRecords:
    @staticmethod
    def btn() -> Literal["""Выгрузить записи начисления бонусов"""]: ...

class AdminReportsAll_Scheduled_posts:
    @staticmethod
    def btn() -> Literal["""Выгрузить запланированные посты"""]: ...

class AdminTeamMenu:
    @staticmethod
    def msg() -> Literal["""Выберите подходящий пункт из меню."""]: ...

class AdminTeamInvite:
    @staticmethod
    def btn() -> Literal["""Добавить в команду"""]: ...
    @staticmethod
    def msg() -> Literal[
        """Отправьте @username или Telegram ID пользователя. 

&lt;i&gt;Перед добавлением в команду пользователь должен запустить бота. Без этого вы не сможете добавить его в команду.&lt;/i&gt;"""
    ]: ...
    @staticmethod
    def success() -> Literal["""Пользователь был успешно добавлен в команду."""]: ...
    @staticmethod
    def unsuccess() -> Literal[
        """Не удалось добавить пользователя в команду. Попробуйте позже, если ошибка повторяется обратитесь в службу поддержки."""
    ]: ...

class AdminTeamSelect:
    role: AdminTeamSelectRole

class AdminTeamSelectRole:
    @staticmethod
    def msg() -> Literal["""Выберите роль для члена вашей команды."""]: ...

class AdminTeamAlready:
    has: AdminTeamAlreadyHas

class AdminTeamAlreadyHas:
    @staticmethod
    def roles() -> Literal["""У этого пользователя уже есть все роли."""]: ...

class AdminTeamKick:
    @staticmethod
    def btn() -> Literal["""Удалить из команды"""]: ...
    @staticmethod
    def msg() -> Literal["""Выберите пользователей для удаления."""]: ...
    @staticmethod
    def success() -> Literal["""Пользователи были успешно удалены из команды."""]: ...
    @staticmethod
    def unsuccess() -> Literal[
        """Не удалось удалить сотрудников. Попробуйте, пожалуйста, позже."""
    ]: ...

class AdminTeamApprove:
    kick: AdminTeamApproveKick

class AdminTeamApproveKick:
    @staticmethod
    def msg() -> Literal[
        """Вы уверены, что хотите удалить из команды выбранных пользователей? 

&lt;i&gt;Удаление из команды никак не повлияет на их профиль клиента. Они смогут пользоваться системой лояльности.&lt;/i&gt;"""
    ]: ...

class AdminBanNot_:
    found: AdminBanNot_Found

class AdminBanNot_Found:
    @staticmethod
    def msg() -> Literal[
        """Пользователь не найден. Проверьте данные и попробуйте еще раз. 

Если все равно не удается найти пользователя, возможно, его нет в базе данных или он не запускал бота."""
    ]: ...

class AdminBanSuccess:
    @staticmethod
    def msg(
        *, i_name, telegram_id
    ) -> Literal["""Пользователь [{ $i_name }-{ $telegram_id }] заблокирован."""]: ...

class AdminBanUnban:
    success: AdminBanUnbanSuccess

    @staticmethod
    def __call__() -> Literal["""Разблокировать"""]: ...

class AdminBanUnbanSuccess:
    @staticmethod
    def msg(
        *, i_name, telegram_id
    ) -> Literal["""Пользователь [{ $i_name }-{ $telegram_id }] разблокирован."""]: ...
