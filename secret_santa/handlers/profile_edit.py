# handlers/profile_edit.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.profile import profile_actions
from keyboards.main import main_menu
from keyboards.cancel import cancel_menu
from db.database import save_profile, get_profile, delete_profile
from states.profile import ProfileState
from utils.text import CANCEL_TEXT
from keyboards.profile_edit import edit_profile_menu

router = Router()

from keyboards.cancel import cancel_menu

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



@router.callback_query(F.data == "edit_profile")
async def edit_profile(cb: CallbackQuery):
    profile = await get_profile(cb.from_user.id)

    if profile[6] == 1:
        return await cb.message.answer("⚠️ Анкета заблокирована.")

    await cb.message.answer(
        "✏️ Что вы хотите отредактировать?",
        reply_markup=edit_profile_menu()
    )

@router.callback_query(F.data.startswith("edit_"))
async def choose_edit_field(cb: CallbackQuery, state: FSMContext):
    field = cb.data.replace("edit_", "")
    await state.set_state(ProfileState.edit_field)
    await state.update_data(edit_field=field)

    names = {
        "name": "Введите новое имя:",
        "wishes": "Введите, что вы хотите получить:",
        "dislikes": "Введите, что НЕ хотите получить:",
        "delivery": "Введите способ доставки:",
        "address": "Введите адрес / пункт выдачи:"
    }

    await cb.message.answer(names[field], reply_markup=cancel_menu())

@router.message(ProfileState.edit_field)
async def save_edited_field(message: Message, state: FSMContext):
    if not message.text:
        return await message.answer("❗ Нужно отправить текст", reply_markup=cancel_menu())

    data = await state.get_data()
    field = data["edit_field"]

    profile = await get_profile(message.from_user.id)
    profile_data = {
        "user_id": profile[0],
        "name": profile[1],
        "wishes": profile[2],
        "dislikes": profile[3],
        "delivery": profile[4],
        "address": profile[5],
    }

    # обновляем нужное поле
    mapping = {
        "name": "name",
        "wishes": "wishes",
        "dislikes": "dislikes",
        "delivery": "delivery",
        "address": "address"
    }
    profile_data[mapping[field]] = message.text

    await save_profile(profile_data)
    await state.clear()

    text = (
        f"✅ Анкета обновлена:\n\n"
        f"👤 Имя: {profile_data['name']}\n"
        f"🎁 Хочу: {profile_data['wishes']}\n"
        f"🚫 Не хочу: {profile_data['dislikes']}\n"
        f"📦 Доставка: {profile_data['delivery']}\n"
        f"📍 Адрес: {profile_data['address']}"
    )

    await message.answer(text, reply_markup=profile_actions())

@router.callback_query(F.data == "delete_profile")
async def delete_profile_cb(cb: CallbackQuery):
    profile = await get_profile(cb.from_user.id)
    if profile[6] == 1:
        return await cb.message.answer("⚠️ Невозможно удалить анкету после распределения.")

    await delete_profile(cb.from_user.id)
    await cb.message.answer("🗑 Анкета удалена", reply_markup=main_menu(False, False))
