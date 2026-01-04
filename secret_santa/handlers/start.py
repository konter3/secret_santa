from aiogram import Router
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from db.database import get_profile, check_distributed, get_pair_for_user
from keyboards.main import main_menu

router = Router()

@router.message()
async def start_command(message: Message):
    user_id = message.from_user.id
    profile = await get_profile(user_id)
    
    if not profile:
        # Если анкеты нет — предлагаем создать
        kb = main_menu(has_profile=False, distributed=False)
        await message.answer(
            "Привет! 👋\nУ тебя ещё нет анкеты. Создай её, чтобы участвовать в Secret Santa.",
            reply_markup=kb
        )
        return

    # Проверяем, было ли распределение
    distributed = await check_distributed()

    if not distributed:
        # Распределение ещё не было — обычное приветствие + анкета
        kb = main_menu(has_profile=True, distributed=False)
        await message.answer(
            f"Привет, {profile[1]}! 👋\nВаша анкета уже сохранена.",
            reply_markup=kb
        )
        return

    # Если распределение есть — показываем получателя
    pair = await get_pair_for_user(user_id, role="santa")
    if not pair:
        # На всякий случай, если что-то пошло не так
        kb = main_menu(has_profile=True, distributed=False)
        await message.answer(
            "Привет! ⚠️ Не удалось найти вашего получателя.",
            reply_markup=kb
        )
        return

    receiver_profile = await get_profile(pair["receiver_id"])
    if not receiver_profile:
        kb = main_menu(has_profile=True, distributed=False)
        await message.answer(
            "Привет! ⚠️ Анкета вашего получателя не найдена.",
            reply_markup=kb
        )
        return

    # Кнопки для общения и отправки трек-номера
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💬 Связь с Сантой", callback_data="chat_santa")],
        [InlineKeyboardButton(text="🎁 Связь с получателем", callback_data="chat_receiver")],
        [InlineKeyboardButton(text="📦 Отправить трек-номер", callback_data="send_track")]
    ])

    text = (
        "🎅 Вам выпал получатель!\n\n"
        f"👤 Имя: {receiver_profile[1]}\n"
        f"🎁 Хочу: {receiver_profile[2]}\n"
        f"🚫 Не хочу: {receiver_profile[3]}\n"
        f"📦 Доставка: {receiver_profile[4]}"
    )

    await message.answer(text, reply_markup=kb)
