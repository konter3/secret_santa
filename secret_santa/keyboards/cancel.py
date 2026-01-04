# keyboards/cancel.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def cancel_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]
        
    ])
