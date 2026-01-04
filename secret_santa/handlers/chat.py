from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.chat import ChatState
from services.relay import relay_message

router = Router()
from keyboards.cancel import cancel_menu
from keyboards.main import main_menu
from db.database import get_profile

# --- Общая отмена ---
@router.callback_query(F.data == "cancel")
async def cancel_cb(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    profile = await get_profile(cb.from_user.id)
    kb = main_menu(has_profile=bool(profile), distributed=False)
    await cb.message.answer("❌ Действие отменено", reply_markup=kb)

@router.callback_query(F.data == "main_menu")
async def main_menu_cb(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    profile = await get_profile(cb.from_user.id)
    kb = main_menu(has_profile=bool(profile), distributed=False)
    await cb.message.answer("🏠 Главное меню", reply_markup=kb)

@router.callback_query(F.data == "chat_santa")
async def chat_santa(cb: CallbackQuery, state: FSMContext):
    await state.set_state(ChatState.chatting)
    await cb.message.answer("💬 Чат с вашим Тайным Сантой открыт. Можно писать текст и пересылать фото.")

@router.callback_query(F.data == "chat_receiver")
async def chat_receiver(cb: CallbackQuery, state: FSMContext):
    await state.set_state(ChatState.chatting)
    await cb.message.answer("💬 Чат с вашим получателем подарка открыт. Можно писать текст и пересылать фото.")

@router.message(ChatState.chatting)
async def chat_relay(message: Message, state: FSMContext):
    await relay_message(message.bot, message.from_user.id, message)
