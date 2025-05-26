from aiogram import F
from aiogram.types import Message
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Button, Group, SwitchTo, Start
from aiogram_dialog.widgets.input import TextInput

from app.bot.states.admin import AdminSG, ReportsSG, TeamSG, BanSG
from app.bot.states.manager.manager import ManagerSG
from .handlers import process_username_or_id
from .getters import get_ban_data, get_common_data, get_kicking_data, get_reports_data, get_team_data
from .filters import filter_message_to_find_username_or_id

admin_dialog = Dialog(
    Window(
        Format("{hello_admin}"),
        Group(
            SwitchTo(
                Format("{reports_btn}"), id="reports_selected", state=AdminSG.reports
            ),
            SwitchTo(Format("{team_menu_btn}"), id="team_selected", state=AdminSG.team),
            Start(
                Format("{manager_role_btn}"),
                id="roles_selected",
                state=ManagerSG,
                data={"is_admin": True},
            ),
            SwitchTo(
                Format("{ban_menu_btn}"), id="ban_menu_selected", state=AdminSG.ban_menu
            ),
            width=2,
        ),
        state=AdminSG.start,
    ),
    # Отчеты
    Window(
        Format("{reports_msg}"),
        Group(
            SwitchTo(
                Format("{reports_users}"),
                id="reports_users_selected",
                state=ReportsSG.users,
            ),
            SwitchTo(
                Format("{reports_scheduled_posts}"),
                id="reports_scheduled_posts_selected",
                state=ReportsSG.posts,
            ),
            SwitchTo(
                Format("{reports_bonus_records}"),
                id="reports_bonus_records_selected",
                state=ReportsSG.bonuses,
            ),
            width=2,
        ),
        SwitchTo(Format("{back}"), id="__back__", state=AdminSG.start),
        state=AdminSG.reports,
        getter=get_reports_data,
    ),
    # Команда
    Window(
        Format("{team_msg}"),
        Group(
            SwitchTo(
                Format("{team_add_btn}"),
                id="add_selected",
                state=TeamSG.invite,
            ),
            SwitchTo(
                Format("{team_kick_btn}"),
                id="kick_selected",
                state=TeamSG.kick
            ),
            width=2,
        ),
        SwitchTo(Format("{back}"), id="__back__", state=AdminSG.start),
        state=AdminSG.team,
        getter=get_team_data,
    ),
    # Управление доступом
    Window(
        Format("{ban_msg}"),
        Group(
            SwitchTo(
                Format("{ban_btn}"),
                id="ban_btn_selected",
                state=BanSG.ban
            ),
            SwitchTo(
                Format("{unban_btn}"),
                id="unban_btn_selected",
                state=BanSG.unban                
            ),
            width=2,
        ),
        SwitchTo(Format("{back}"), id="__back__", state=AdminSG.start),
        state=AdminSG.ban_menu,
        getter=get_ban_data,
    ),
    
    # Выдача отчетов
    # Window(),
    
    # Управление командой
    Window(
        Format("{team_invite_msg}"),
        TextInput(
            id="processing_invite_new_member",
            on_success=process_username_or_id, 
            filter=filter_message_to_find_username_or_id
        ),
        state=TeamSG.invite,
        getter=get_team_data
    ),
    Window(
        Format("{team_kick_msg}"),

        state=TeamSG.kick,
        getter=get_kicking_data
    ),
    getter=get_common_data,
)
