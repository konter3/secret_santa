# keyboards/main.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu(has_profile: bool, distributed: bool, is_admin: bool = False):
    kb = []
    if not has_profile:
        kb.append([InlineKeyboardButton(text="➕ Создать анкету", callback_data="create_profile")])
    else:
        kb.append([InlineKeyboardButton(text="👤 Моя анкета", callback_data="view_profile")])

    if distributed:
        kb.append([InlineKeyboardButton(text="💬 Связь с Сантой", callback_data="chat_santa")])
        kb.append([InlineKeyboardButton(text="🎁 Связь с получателем", callback_data="chat_receiver")])
        kb.append([InlineKeyboardButton(text="📦 Отправить трек-номер", callback_data="send_track")])

    if is_admin:
        kb.append([InlineKeyboardButton(
            text="🛠 Мастерская Санты",
            callback_data="admin_menu"
        )])

    return InlineKeyboardMarkup(inline_keyboard=kb)
