from aiogram import Router, F
from aiogram.types import Message
from db.database import get_profile
from keyboards.main import main_menu
from utils.text import WELCOME_TEXT

router = Router()

@router.message(F.text == "/start")
async def start_bot(message: Message):
    profile = await get_profile(message.from_user.id)
    kb = main_menu(has_profile=bool(profile), distributed=False)
    await message.answer(WELCOME_TEXT, reply_markup=kb)
