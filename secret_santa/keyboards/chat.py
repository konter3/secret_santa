from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def chat_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 В меню", callback_data="main_menu")]
    ])
