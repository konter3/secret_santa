# keyboards/profile_edit.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def edit_profile_menu(extra_buttons: list[list[InlineKeyboardButton]] = None) -> InlineKeyboardMarkup:
    """
    Кнопки для редактирования анкеты пользователя.
    Можно добавить дополнительные кнопки через extra_buttons.
    """
    buttons = [
        [InlineKeyboardButton(text="👤 Имя", callback_data="edit_name")],
        [InlineKeyboardButton(text="🎁 Хочу получить", callback_data="edit_wishes")],
        [InlineKeyboardButton(text="🚫 Не хочу получить", callback_data="edit_dislikes")],
        [InlineKeyboardButton(text="📦 Способ доставки", callback_data="edit_delivery")],
        [InlineKeyboardButton(text="📍 Адрес", callback_data="edit_address")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="view_profile")]
    ]

    if extra_buttons:
        buttons.extend(extra_buttons)

    return InlineKeyboardMarkup(inline_keyboard=buttons)
