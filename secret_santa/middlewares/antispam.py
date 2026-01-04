import time
from aiogram import BaseMiddleware

class AntiSpamMiddleware(BaseMiddleware):
    def __init__(self):
        self.users = {}

    async def __call__(self, handler, event, data):
        uid = event.from_user.id
        now = time.time()
        if uid in self.users and now - self.users[uid] < 60:
            await event.answer("⏳ Не чаще одного сообщения в минуту")
            return
        self.users[uid] = now
        return await handler(event, data)
