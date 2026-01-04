from aiogram.fsm.state import StatesGroup, State

class ChatState(StatesGroup):
    santa_chat = State()
    receiver_chat = State()
