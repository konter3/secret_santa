import logging
from aiogram import BaseMiddleware

class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        logging.info(f"{event.from_user.id} -> {event}")
        return await handler(event, data)
