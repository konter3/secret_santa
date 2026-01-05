# keyboards/admin.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_menu(distributed: bool = False):
    """
    Клавиатура для админ-панели.
    Если распределение уже выполнено, можно скрыть кнопку "Распределить Сант".
    """
    buttons = []

    if not distributed:
        buttons.append([InlineKeyboardButton(
            text="🎲 Распределить Санту",
            callback_data="distribute"
        )])

    buttons.append([InlineKeyboardButton(
        text="🏠 В меню",
        callback_data="main_menu"
    )])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
