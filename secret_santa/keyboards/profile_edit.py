from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def edit_profile_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👤 Имя", callback_data="edit_name")],
        [InlineKeyboardButton(text="🎁 Хочу получить", callback_data="edit_wishes")],
        [InlineKeyboardButton(text="🚫 Не хочу получить", callback_data="edit_dislikes")],
        [InlineKeyboardButton(text="📦 Способ доставки", callback_data="edit_delivery")],
        [InlineKeyboardButton(text="📍 Адрес", callback_data="edit_address")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="view_profile")]
    ])
