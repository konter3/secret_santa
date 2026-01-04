from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Количество анкет", callback_data="count_profiles")],
        [InlineKeyboardButton(text="🎲 Распределить Сант", callback_data="distribute")]
    ])
