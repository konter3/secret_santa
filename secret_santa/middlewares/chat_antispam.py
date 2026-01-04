import time
from aiogram import BaseMiddleware
from states.chat import ChatState
from aiogram.fsm.context import FSMContext

class ChatAntiSpamMiddleware(BaseMiddleware):
    def __init__(self, cooldown: int = 10):
        super().__init__()
        self.users = {}  # {user_id: last_message_time}
        self.cooldown = cooldown  # минимальный интервал между сообщениями (сек)

    async def __call__(self, handler, event, data):
        """
        Middleware для ограничения частоты сообщений в анонимных чатах.
        Применяется только для состояний santa_chat и receiver_chat.
        """
        # Определяем user_id
        user_id = getattr(event.from_user, "id", None)
        if not user_id:
            # Нет from_user — пропускаем
            return await handler(event, data)

        # Проверяем FSM state
        state: FSMContext = data.get("state")
        if not state:
            return await handler(event, data)

        current_state = await state.get_state()
        # Если пользователь не в чате с Сантой или с получателем — антиспам не применяется
        if current_state not in [ChatState.santa_chat.state, ChatState.receiver_chat.state]:
            return await handler(event, data)

        # Ограничение по времени
        now = time.time()
        last_time = self.users.get(user_id, 0)
        if now - last_time < self.cooldown:
            if hasattr(event, "answer"):
                await event.answer(f"⏳ Можно писать не чаще одного сообщения каждые {self.cooldown} секунд")
            return  # Прерываем обработку хендлера

        # Обновляем время последнего сообщения
        self.users[user_id] = now
        return await handler(event, data)
