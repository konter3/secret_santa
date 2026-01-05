# handlers/start.py
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from db.database import get_profile, check_distributed, get_pair_by_giver, get_pair_by_receiver
from utils.text import REPEAT_TEXT

router = Router()

@router.message(F.text == "/start")  # правильный синтаксис для 3.x
async def start_command(message: Message):
    user_id = message.from_user.id
    profile = await get_profile(user_id)

    if not profile:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="➕ Создать анкету", callback_data="create_profile")]
        ])
        await message.answer(
            "Привет! 👋\nУ тебя ещё нет анкеты. Создай её, чтобы участвовать в Тайном Санте.",
            reply_markup=kb
        )
        return

    distributed = await check_distributed()

    if not distributed:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="👤 Моя анкета", callback_data="view_profile")]
        ])
        await message.answer(
            f"Привет, {profile[1]}! 👋\nВаша анкета уже сохранена.",
            reply_markup=kb
        )
        return

    pair_as_santa = await get_pair_by_giver(user_id)
    pair_as_receiver = await get_pair_by_receiver(user_id)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 Отправить трек-номер", callback_data="send_track")],
        [InlineKeyboardButton(text="📍 Посмотреть мой трек-номер", callback_data="view_track")]
    ])

    await message.answer(REPEAT_TEXT)
    text = f"Привет, {profile[1]}! 🎅\n\n"

    if pair_as_santa:
        receiver_profile = await get_profile(pair_as_santa["receiver_id"])
        if receiver_profile:
            text += (
                "🎁 Ваш получатель:\n"
                f"👤 Имя: {receiver_profile[1]}\n"
                f"🎁 Хочу: {receiver_profile[2]}\n"
                f"🚫 Не хочу: {receiver_profile[3]}\n"
                f"📦 Доставка: {receiver_profile[4]}\n"
                f"📍 Адрес: {profile[5]}"
            )
    elif pair_as_receiver:
        santa_profile = await get_profile(pair_as_receiver["giver_id"])
        if santa_profile:
            text += (
                "🎁 Вам дарит подарок:\n"
                f"👤 Имя: {santa_profile[1]}\n"
                f"🎁 Хочу: {santa_profile[2]}\n"
                f"🚫 Не хочу: {santa_profile[3]}\n"
                f"📦 Доставка: {santa_profile[4]}\n"
                f"📍 Адрес: {profile[5]}"
            )
    else:
        text += "⚠️ Пара не найдена."

    await message.answer(text, reply_markup=kb)
