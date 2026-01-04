# keyboards/admin.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Распределить Сант", callback_data="distribute")]
    ])
