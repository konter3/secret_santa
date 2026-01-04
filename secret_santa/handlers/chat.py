from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.chat import ChatState
from db.database import get_pair_for_user, get_chat_history, save_chat_message
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
    kb = main_menu(has_profile=bool(profile), distributed=False, is_admin=is_admin)
    await cb.message.answer("❌ Действие отменено", reply_markup=kb)


@router.callback_query(F.data == "main_menu")
async def main_menu_cb(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    profile = await get_profile(cb.from_user.id)
    is_admin = cb.from_user.id in ADMINS
    kb = main_menu(has_profile=bool(profile), distributed=False, is_admin=is_admin)
    await cb.message.answer("🏠 Главное меню", reply_markup=kb)


# --- Открытие чата с Сантой ---
@router.callback_query(F.data == "chat_santa")
async def open_santa_chat(cb: CallbackQuery, state: FSMContext):
    user_id = cb.from_user.id
    bot = cb.bot

    # Получаем Санту для этого пользователя
    pair = await get_pair_for_user(user_id, role="receiver")
    if not pair or "giver_id" not in pair:
        return await cb.message.answer("❌ Чат недоступен")

    # История сообщений
    messages = await get_chat_history(user_id, role="santa")

    await cb.message.answer("💬 Чат с Сантой")

    for msg in messages:
        if msg["message_type"] == "text":
            await bot.send_message(user_id, msg["content"])
        elif msg["message_type"] == "photo":
            await bot.send_photo(user_id, msg["file_id"], caption=msg["content"])
        elif msg["message_type"] == "document":
            await bot.send_document(user_id, msg["file_id"])

    await state.set_state(ChatState.santa_chat)
    await cb.message.answer("✍️ Можете писать сообщение", reply_markup=cancel_menu())


# --- Открытие чата с получателем ---
@router.callback_query(F.data == "chat_receiver")
async def open_receiver_chat(cb: CallbackQuery, state: FSMContext):
    user_id = cb.from_user.id
    bot = cb.bot

    pair = await get_pair_for_user(user_id, role="santa")
    if not pair or "receiver_id" not in pair:
        return await cb.message.answer("❌ Чат недоступен")

    messages = await get_chat_history(user_id, role="receiver")

    await cb.message.answer("💬 Чат с получателем подарка")

    for msg in messages:
        if msg["message_type"] == "text":
            await bot.send_message(user_id, msg["content"])
        elif msg["message_type"] == "photo":
            await bot.send_photo(user_id, msg["file_id"], caption=msg["content"])
        elif msg["message_type"] == "document":
            await bot.send_document(user_id, msg["file_id"])

    await state.set_state(ChatState.receiver_chat)
    await cb.message.answer("✍️ Можете писать сообщение", reply_markup=cancel_menu())


# --- Обработка сообщений Санты ---
@router.message(ChatState.santa_chat)
async def santa_chat_message(message: Message, state: FSMContext):
    pair = await get_pair_for_user(message.from_user.id, role="santa")
    if not pair or "receiver_id" not in pair:
        return await message.answer("⚠️ Пара не найдена.")

    receiver_id = pair["receiver_id"]

    await forward_message(message.from_user.id, receiver_id, "santa", message)


# --- Обработка сообщений получателя ---
@router.message(ChatState.receiver_chat)
async def receiver_chat_message(message: Message, state: FSMContext):
    pair = await get_pair_for_user(message.from_user.id, role="receiver")
    if not pair or "giver_id" not in pair:
        return await message.answer("⚠️ Пара не найдена.")

    santa_id = pair["giver_id"]

    await forward_message(message.from_user.id, santa_id, "receiver", message)


# --- Функция пересылки сообщений ---
async def forward_message(from_user, to_user, role, message: Message):
    bot = message.bot

    # Текст
    if message.text:
        await bot.send_message(to_user, message.text)
        await save_chat_message(from_user, to_user, role, "text", message.text)

    # Фото
    elif message.photo:
        file_id = message.photo[-1].file_id
        await bot.send_photo(to_user, file_id, caption=message.caption)
        await save_chat_message(from_user, to_user, role, "photo", message.caption, file_id)

    # Документ
    elif message.document:
        await bot.send_document(to_user, message.document.file_id)
        await save_chat_message(from_user, to_user, role, "document", None, message.document.file_id)
