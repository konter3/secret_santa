from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.tracking import TrackState
from db.database import save_track_number, get_pair_by_user

router = Router()

@router.callback_query(F.data == "send_track")
async def send_track_cb(cb: CallbackQuery, state: FSMContext):
    await state.set_state(TrackState.waiting_track)
    await cb.message.answer("Введите трек-номер или напишите «Вручу лично»")

@router.message(TrackState.waiting_track)
async def track_input(message: Message, state: FSMContext):
    if not message.text:
        return await message.answer("❗ Только текст")
    pair = await get_pair_by_user(message.from_user.id)
    if not pair:
        return await message.answer("Ошибка: пара не найдена")
    await save_track_number(pair["receiver_id"], message.text)
    await message.bot.send_message(pair["receiver_id"], f"📦 Трек-номер: {message.text}")
    await state.clear()
    await message.answer("✅ Трек-номер отправлен")
