from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from db.database import get_profile, check_distributed, get_pair_by_giver, get_pair_by_receiver
from utils.text import WELCOME_TEXT, REPEAT_TEXT
from config import ADMINS
from keyboards.main import main_menu

router = Router()

@router.message(F.text == "/start")
async def start_command(message: Message):
    user_id = message.from_user.id
    profile = await get_profile(user_id)
    is_admin = user_id in ADMINS

    # Проверяем, было ли распределение
    distributed = await check_distributed()

    # Составляем клавиатуру через функцию
    kb = main_menu(has_profile=bool(profile), distributed=distributed, is_admin=is_admin)

    # Если анкеты нет — выводим приветствие и кнопку создать
    if not profile:
        await message.answer(WELCOME_TEXT, reply_markup=kb)
        return

    # Анкета есть, но распределение еще не было
    if not distributed:
        await message.answer(f"Привет, {profile[1]}! 👋\nВаша анкета уже сохранена.", reply_markup=kb)
        return

    # Если распределение есть — показываем информацию о получателе
    pair_as_santa = await get_pair_by_giver(user_id)
    pair_as_receiver = await get_pair_by_receiver(user_id)

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
                f"📍 Адрес: {receiver_profile[5]}"
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

    await message.answer(REPEAT_TEXT)
    await message.answer(text, reply_markup=kb)
