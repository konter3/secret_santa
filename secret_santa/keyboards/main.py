# keyboards/main.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu(has_profile: bool, distributed: bool, is_admin: bool = False):
    """
    Главное меню пользователя.
    
    has_profile: есть ли анкета
    distributed: были ли распределены пары
    is_admin: является ли пользователь админом
    """
    kb = []

    # Анкета
    if not has_profile:
        kb.append([InlineKeyboardButton(text="➕ Создать анкету", callback_data="create_profile")])
    else:
        kb.append([InlineKeyboardButton(text="👤 Моя анкета", callback_data="view_profile")])

    # После распределения показываем кнопки для трек-номера
    if distributed:
        kb.append([InlineKeyboardButton(text="📦 Отправить трек-номер", callback_data="send_track")])
        kb.append([InlineKeyboardButton(text="📦 Посмотреть мой трек-номер", callback_data="view_track")])

    # Админка
    if is_admin:
        kb.append([InlineKeyboardButton(text="🛠 Мастерская Санты", callback_data="admin_menu")])

    return InlineKeyboardMarkup(inline_keyboard=kb)
