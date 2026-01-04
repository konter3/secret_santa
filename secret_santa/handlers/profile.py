from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.profile import profile_actions
from keyboards.main import main_menu
from db.database import save_profile, get_profile, delete_profile
from states.profile import ProfileState
from utils.text import CANCEL_TEXT

router = Router()

from keyboards.cancel import cancel_menu


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

# --- Создание анкеты ---
@router.callback_query(F.data == "create_profile")
async def start_profile(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    await cb.message.answer("Введите ваше имя:")
    await state.set_state(ProfileState.name)

@router.message(ProfileState.name)
async def step_name(message: Message, state: FSMContext):
    if message.text.lower() in ["❌ отмена", "🏠 главное меню"]:
        await state.clear()
        profile = await get_profile(message.from_user.id)
        kb = main_menu(has_profile=bool(profile), distributed=False)
        return await message.answer("❌ Действие отменено", reply_markup=kb)

    if not message.text:
        return await message.answer("❗ Только текст")
    await state.update_data(name=message.text)
    await message.answer("Что бы вы хотели получить?")
    await state.set_state(ProfileState.wishes)

@router.message(ProfileState.wishes)
async def step_wishes(message: Message, state: FSMContext):
    if message.text.lower() in ["❌ отмена", "🏠 главное меню"]:
        await state.clear()
        profile = await get_profile(message.from_user.id)
        kb = main_menu(has_profile=bool(profile), distributed=False)
        return await message.answer("❌ Действие отменено", reply_markup=kb)
    if not message.text:
        return await message.answer("❗ Только текст")
    await state.update_data(wishes=message.text)
    await message.answer("Что НЕ хотели бы получить?")
    await state.set_state(ProfileState.dislikes)

@router.message(ProfileState.dislikes)
async def step_dislikes(message: Message, state: FSMContext):
    if message.text.lower() in ["❌ отмена", "🏠 главное меню"]:
        await state.clear()
        profile = await get_profile(message.from_user.id)
        kb = main_menu(has_profile=bool(profile), distributed=False)
        return await message.answer("❌ Действие отменено", reply_markup=kb)
    if not message.text:
        return await message.answer("❗ Только текст")
    await state.update_data(dislikes=message.text)
    await message.answer("Способ получения (почта / ozon / wb):")
    await state.set_state(ProfileState.delivery)

@router.message(ProfileState.delivery)
async def step_delivery(message: Message, state: FSMContext):
    if message.text.lower() in ["❌ отмена", "🏠 главное меню"]:
        await state.clear()
        profile = await get_profile(message.from_user.id)
        kb = main_menu(has_profile=bool(profile), distributed=False)
        return await message.answer("❌ Действие отменено", reply_markup=kb)
    if not message.text:
        return await message.answer("❗ Только текст")
    await state.update_data(delivery=message.text)
    await message.answer("Адрес доставки / пункт выдачи:")
    await state.set_state(ProfileState.address)

@router.message(ProfileState.address)
async def step_address(message: Message, state: FSMContext):
    if message.text.lower() in ["❌ отмена", "🏠 главное меню"]:
        await state.clear()
        profile = await get_profile(message.from_user.id)
        kb = main_menu(has_profile=bool(profile), distributed=False)
        return await message.answer("❌ Действие отменено", reply_markup=kb)
    if not message.text:
        return await message.answer("❗ Только текст")
    data = await state.get_data()
    data["address"] = message.text
    await save_profile({
        "user_id": message.from_user.id,
        **data,
        "locked": 0
    })
    await state.clear()
    kb = main_menu(has_profile=True, distributed=False)
    await message.answer("✅ Анкета создана", reply_markup=kb)

# --- Просмотр и редактирование ---
@router.callback_query(F.data == "view_profile")
async def view_profile(cb: CallbackQuery):
    profile = await get_profile(cb.from_user.id)

    if profile[6] == 1:  # locked
        return await cb.message.answer("⚠️ Анкета заблокирована. После распределения редактирование невозможно.")

    if not profile:
        return await cb.message.answer("Анкета не найдена.")
    text = (
        f"👤 Имя: {profile[1]}\n"
        f"🎁 Хочу: {profile[2]}\n"
        f"🚫 Не хочу: {profile[3]}\n"
        f"📦 Доставка: {profile[4]}\n"
        f"📍 Адрес: {profile[5]}"
    )
    await cb.message.answer(text, reply_markup=profile_actions())

@router.callback_query(F.data == "delete_profile")
async def delete_profile_cb(cb: CallbackQuery):
    profile = await get_profile(cb.from_user.id)
    if profile[6] == 1:
        return await cb.message.answer("⚠️ Невозможно удалить анкету после распределения.")

    await delete_profile(cb.from_user.id)
    await cb.message.answer("🗑 Анкета удалена", reply_markup=main_menu(False, False))
