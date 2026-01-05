# handlers/admin.py
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from config import ADMINS
from db.database import count_profiles
from services.santa_distribution import distribute
from keyboards.admin import admin_menu
from keyboards.main import main_menu
from db.database import get_profile

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
async def distribute_cb(cb: CallbackQuery, bot: Bot):
    pairs = await distribute()

    if not pairs:
        return await cb.message.answer("❗ Недостаточно участников")

    for santa_id, receiver_id in pairs:
        profile = await get_profile(receiver_id)

        if not profile:
            continue

        text = (
            "🎅 Вам выпал получатель!\n\n"
            f"👤 Имя: {profile[1]}\n"
            f"🎁 Хочу: {profile[2]}\n"
            f"🚫 Не хочу: {profile[3]}\n"
            f"📦 Доставка: {profile[4]}"
        )

        await bot.send_message(
            santa_id,
            text,
            reply_markup=main_menu(
                has_profile=True,
                distributed=True,
                is_admin=santa_id in ADMINS
            )
        )

    await cb.message.answer("✅ Распределение завершено")