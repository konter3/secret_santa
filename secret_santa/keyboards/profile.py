from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def profile_actions():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✏️ Редактировать", callback_data="edit_profile")],
        [InlineKeyboardButton(text="🗑 Удалить", callback_data="delete_profile")],
        [InlineKeyboardButton(text="🏠 В меню", callback_data="main_menu")]
    ])
