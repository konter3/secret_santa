from aiogram import Router, F
from aiogram.types import CallbackQuery
from config import ADMINS
from db.database import count_profiles
from services.santa_distribution import distribute

router = Router()

@router.callback_query(F.data == "count_profiles")
async def count_cb(cb: CallbackQuery):
    if cb.from_user.id not in ADMINS:
        return
    total = await count_profiles()
    await cb.message.answer(f"📊 Всего анкет: {total}")

@router.callback_query(F.data == "distribute")
async def distribute_cb(cb: CallbackQuery):
    if cb.from_user.id not in ADMINS:
        return
    await distribute()
    await cb.message.answer("🎲 Распределение выполнено. Пользователи получили свои пары.")
