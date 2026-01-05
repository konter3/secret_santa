# keyboards/chat.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def chat_keyboard(extra_buttons: list[list[InlineKeyboardButton]] = None) -> InlineKeyboardMarkup:
    """
    Клавиатура для чата с кнопкой "В меню".
    Можно добавить дополнительные кнопки через extra_buttons.
    """
    buttons = [[InlineKeyboardButton(text="🏠 В меню", callback_data="main_menu")]]
    
    if extra_buttons:
        buttons.extend(extra_buttons)
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)
