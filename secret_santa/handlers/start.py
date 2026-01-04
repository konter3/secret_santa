from aiogram import Router, F
from aiogram.types import Message
from db.database import get_profile
from keyboards.main import main_menu
from utils.text import WELCOME_TEXT
from config import ADMINS

router = Router()

@router.message(F.text == "/start")
async def start_bot(message: Message):
    profile = await get_profile(message.from_user.id)
    is_admin = message.from_user.id in ADMINS

    kb = main_menu(
        has_profile=bool(profile),
        distributed=False,
        is_admin=is_admin
    )
    await message.answer(WELCOME_TEXT, reply_markup=kb)
