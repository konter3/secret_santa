# keyboards/cancel.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def cancel_menu(extra_buttons: list[list[InlineKeyboardButton]] = None) -> InlineKeyboardMarkup:
    """
    Клавиатура отмены.
    Можно добавить дополнительные кнопки через extra_buttons.
    """
    buttons = [[InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]]
    
    if extra_buttons:
        buttons.extend(extra_buttons)
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)
