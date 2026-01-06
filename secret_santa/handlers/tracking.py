# handlers/tracking.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.tracking import TrackState
from db.database import get_pair_by_giver, get_pair_by_receiver, save_track_number, get_profile
from keyboards.cancel import cancel_menu
from keyboards.main import main_menu
from config import ADMINS

router = Router()

# --- Общая отмена ---
@router.callback_query(F.data == "cancel")
async def cancel_cb(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    profile = await get_profile(cb.from_user.id)
    is_admin = cb.from_user.id in ADMINS
    kb = main_menu(has_profile=bool(profile), distributed=True, is_admin=is_admin)
    await cb.message.answer("❌ Действие отменено", reply_markup=kb)

@router.callback_query(F.data == "main_menu")
async def main_menu_cb(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    profile = await get_profile(cb.from_user.id)
    is_admin = cb.from_user.id in ADMINS
    kb = main_menu(has_profile=bool(profile), distributed=True, is_admin=is_admin)
    await cb.message.answer("🏠 Главное меню", reply_markup=kb)


# --- Отправка трек-номера ---
@router.callback_query(F.data == "send_track")
async def send_track_cb(cb: CallbackQuery, state: FSMContext):
    pair = await get_pair_by_giver(cb.from_user.id)
    if not pair:
        return await cb.message.answer("⚠️ Получатель не найден")

    await state.set_state(TrackState.waiting_track)
    await cb.message.answer(
        f"Введите трек-номер для {pair['receiver_id']} или напишите «Вручу лично»",
        reply_markup=cancel_menu()
    )

@router.message(TrackState.waiting_track)
async def track_input(message: Message, state: FSMContext):
    if not message.text:
        return await message.answer("❗ Нужно отправить текст")
    
    pair = await get_pair_by_giver(message.from_user.id)
    if not pair:
        await state.clear()
        return await message.answer("⚠️ Получатель не найден")

    # Сохраняем трек
    await save_track_number(message.from_user.id, message.text)
    
    # Отправляем получателю
    await message.bot.send_message(
        pair["receiver_id"],
        f"📦 Вам отправлен трек-номер для получения подарка: {message.text}"
    )
    await state.clear()
    await message.answer("✅ Трек-номер отправлен", reply_markup=main_menu(has_profile=True, distributed=True))


# --- Просмотр своего трек-номера ---
@router.callback_query(F.data == "view_track")
async def view_track_cb(cb: CallbackQuery):
    pair = await get_pair_by_receiver(cb.from_user.id)
    if not pair or not pair["track_number"]:
        return await cb.message.answer("⚠️ Санта ещё не отправил подарок")

    await cb.message.answer(f"📦 Ваш трек-номер для получения подарка: {pair['track_number']}", reply_markup=main_menu(has_profile=True, distributed=True))
