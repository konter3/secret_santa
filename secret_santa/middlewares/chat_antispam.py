import time
from aiogram import BaseMiddleware
from states.chat import ChatState
from aiogram.fsm.context import FSMContext

class ChatAntiSpamMiddleware(BaseMiddleware):
    def __init__(self):
        self.users = {}  # {user_id: last_message_time}

    async def __call__(self, handler, event, data):
        """
        event — это уже Message или CallbackQuery, поэтому
        проверяем тип
        """
        # Определяем user_id
        user_id = None
        if hasattr(event, "from_user") and event.from_user:
            user_id = event.from_user.id
        else:
            # Нет from_user — пропускаем обработку
            return await handler(event, data)

        # Проверяем FSM state
        state: FSMContext = data.get("state")
        if not state:
            return await handler(event, data)

        current_state = await state.get_state()
        if current_state != ChatState.chatting.state:
            # Не в анонимном чате — антиспам не применяется
            return await handler(event, data)

        # Ограничение по времени
        now = time.time()
        last_time = self.users.get(user_id, 0)

        if now - last_time < 60:
            # Сообщение о спаме
            if hasattr(event, "answer"):
                await event.answer("⏳ Можно писать не чаще одного сообщения в минуту")
            return  # Прерываем обработку хендлера

        # Обновляем время последнего сообщения
        self.users[user_id] = now
        return await handler(event, data)
