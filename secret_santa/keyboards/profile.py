# keyboards/profile.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def profile_actions(extra_buttons: list[list[InlineKeyboardButton]] = None) -> InlineKeyboardMarkup:
    """
    Кнопки для просмотра/редактирования профиля.
    Можно добавить дополнительные кнопки через extra_buttons.
    """
    buttons = [
        [InlineKeyboardButton(text="✏️ Редактировать", callback_data="edit_profile")],
        [InlineKeyboardButton(text="🗑 Удалить", callback_data="delete_profile")],
        [InlineKeyboardButton(text="🏠 В меню", callback_data="main_menu")]
    ]

    if extra_buttons:
        buttons.extend(extra_buttons)

    return InlineKeyboardMarkup(inline_keyboard=buttons)
