from typing import TYPE_CHECKING, Dict


from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Multiselect

from fluentogram import TranslatorRunner


from app.bot.utils.enums.role import UserType

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner  # type:ignore
    
async def content_data(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    **kwargs,
) -> Dict[str, str]:
    return {
        "main_menu": i18n.main.menu(),
        "content_hello_msg": i18n.content.hello(),
        "content_bot_btn": i18n.content.bot.btn(),
        "content_channel_btn": i18n.content.channel.btn(),
        "delete_btn": i18n.delete(),
        "edit_btn": i18n.edit(),
    }
    
    
async def content_bot_data(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    **kwargs,
) -> Dict[str, str]:
    return {
        
    }
    

async def content_channel_data(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    **kwargs,
) -> Dict[str, str]:
    return {
        
    }