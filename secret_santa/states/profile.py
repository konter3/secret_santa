from aiogram.fsm.state import StatesGroup, State

class ProfileState(StatesGroup):
    name = State()
    wishes = State()
    dislikes = State()
    delivery = State()
    address = State()
    preview = State()

    edit_field = State()