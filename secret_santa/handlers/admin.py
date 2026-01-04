from aiogram import Router, F
from aiogram.types import CallbackQuery
from config import ADMINS
from db.database import count_profiles
from services.santa_distribution import distribute
from keyboards.admin import admin_menu

router = Router()

@router.callback_query(F.data == "admin_menu")
async def admin_panel(cb: CallbackQuery):
    if cb.from_user.id not in ADMINS:
        return await cb.answer("⛔ Нет доступа", show_alert=True)

    total = await count_profiles()
    await cb.message.answer(
        "🛠 Админ-панель\n\n"
        f"📊 Всего анкет: {total}",
        reply_markup=admin_menu()
    )


@router.callback_query(F.data == "distribute")
async def distribute_cb(cb: CallbackQuery):
    if cb.from_user.id not in ADMINS:
        return
    await distribute()
    await cb.message.answer("🎲 Распределение выполнено. Пользователи получили свои пары.")
