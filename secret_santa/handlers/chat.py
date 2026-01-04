from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.chat import ChatState
from services.relay import relay_message

router = Router()

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
