from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def cancel_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
    ])
