# handlers/profile.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.profile import profile_actions
from keyboards.main import main_menu
from keyboards.cancel import cancel_menu
from db.database import save_profile, get_profile, delete_profile, check_distributed
from states.profile import ProfileState
from utils.text import WELCOME_TEXT
from config import ADMINS
router = Router()

from keyboards.cancel import cancel_menu


# --- Общая отмена ---
@router.callback_query(F.data == "cancel")
async def cancel_cb(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    profile = await get_profile(cb.from_user.id)
    is_admin = cb.from_user.id in ADMINS

    distributed = await check_distributed()

    kb = main_menu(
        has_profile=bool(profile),
        distributed=distributed,
        is_admin=is_admin
    )

    await cb.message.answer("❌ Действие отменено", reply_markup=kb)

@router.callback_query(F.data == "main_menu")
async def main_menu_cb(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    profile = await get_profile(cb.from_user.id)

    is_admin = cb.from_user.id in ADMINS

    distributed = await check_distributed()

    kb = main_menu(
        has_profile=bool(profile),
        distributed=distributed,
        is_admin=is_admin
    )
    await cb.message.answer("🏠 Главное меню", reply_markup=kb)

# --- Создание анкеты ---
@router.callback_query(F.data == "create_profile")
async def start_profile(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    await cb.message.answer(WELCOME_TEXT)
    await cb.message.answer("Введите ваше имя:", reply_markup=cancel_menu())
    await state.set_state(ProfileState.name)

@router.message(ProfileState.name)
async def step_name(message: Message, state: FSMContext):
    if message.text.lower() in ["❌ отмена", "🏠 главное меню"]:
        await state.clear()
        profile = await get_profile(message.from_user.id)
        is_admin = message.from_user.id in ADMINS

        distributed = await check_distributed()

        kb = main_menu(
            has_profile=bool(profile),
            distributed=distributed,
            is_admin=is_admin
        )
        return await message.answer("❌ Действие отменено", reply_markup=kb)

    if not message.text:
        return await message.answer("❗ Только текст", reply_markup=cancel_menu())
    await state.update_data(name=message.text)
    await message.answer("Что бы вы хотели получить?", reply_markup=cancel_menu())
    await state.set_state(ProfileState.wishes)

@router.message(ProfileState.wishes)
async def step_wishes(message: Message, state: FSMContext):
    if message.text.lower() in ["❌ отмена", "🏠 главное меню"]:
        await state.clear()
        profile = await get_profile(message.from_user.id)
        is_admin = message.from_user.id in ADMINS

        distributed = await check_distributed()

        kb = main_menu(
            has_profile=bool(profile),
            distributed=distributed,
            is_admin=is_admin
        )
        return await message.answer("❌ Действие отменено", reply_markup=kb)
    if not message.text:
        return await message.answer("❗ Только текст", reply_markup=cancel_menu())
    await state.update_data(wishes=message.text)
    await message.answer("Что НЕ хотели бы получить?", reply_markup=cancel_menu())
    await state.set_state(ProfileState.dislikes)

@router.message(ProfileState.dislikes)
async def step_dislikes(message: Message, state: FSMContext):
    if message.text.lower() in ["❌ отмена", "🏠 главное меню"]:
        await state.clear()
        profile = await get_profile(message.from_user.id)
        is_admin = message.from_user.id in ADMINS

        distributed = await check_distributed()

        kb = main_menu(
            has_profile=bool(profile),
            distributed=distributed,
            is_admin=is_admin
        )
        return await message.answer("❌ Действие отменено", reply_markup=kb)
    if not message.text:
        return await message.answer("❗ Только текст", reply_markup=cancel_menu())
    await state.update_data(dislikes=message.text)
    await message.answer("Способ получения (почта / ozon / wb):", reply_markup=cancel_menu())
    await state.set_state(ProfileState.delivery)

@router.message(ProfileState.delivery)
async def step_delivery(message: Message, state: FSMContext):
    if message.text.lower() in ["❌ отмена", "🏠 главное меню"]:
        await state.clear()
        profile = await get_profile(message.from_user.id)
        is_admin = message.from_user.id in ADMINS

        distributed = await check_distributed()

        kb = main_menu(
            has_profile=bool(profile),
            distributed=distributed,
            is_admin=is_admin
        )
        return await message.answer("❌ Действие отменено", reply_markup=kb)
    if not message.text:
        return await message.answer("❗ Только текст", reply_markup=cancel_menu())
    await state.update_data(delivery=message.text)
    await message.answer("Адрес доставки / пункт выдачи:", reply_markup=cancel_menu())
    await state.set_state(ProfileState.address)

@router.message(ProfileState.address)
async def step_address(message: Message, state: FSMContext):
    if message.text.lower() in ["❌ отмена", "🏠 главное меню"]:
        await state.clear()
        profile = await get_profile(message.from_user.id)
        is_admin = message.from_user.id in ADMINS

        distributed = await check_distributed()

        kb = main_menu(
            has_profile=bool(profile),
            distributed=distributed,
            is_admin=is_admin
        )
        return await message.answer("❌ Действие отменено", reply_markup=kb)
    if not message.text:
        return await message.answer("❗ Только текст", reply_markup=cancel_menu())
    data = await state.get_data()
    data["address"] = message.text
    await save_profile({
        "user_id": message.from_user.id,
        **data,
        "locked": 0
    })
    await state.clear()

    profile = await get_profile(message.from_user.id)
    is_admin = message.from_user.id in ADMINS

    distributed = await check_distributed()

    kb = main_menu(
        has_profile=bool(profile),
        distributed=distributed,
        is_admin=is_admin
    )
    await message.answer("✅ Анкета создана", reply_markup=kb)