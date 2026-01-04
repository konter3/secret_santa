import logging
from aiogram import BaseMiddleware
from aiogram.types import Update

class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data):
        # Определяем откуда пользователь
        user_id = None
        if event.message:
            user_id = event.message.from_user.id
        elif event.callback_query:
            user_id = event.callback_query.from_user.id
        elif event.inline_query:
            user_id = event.inline_query.from_user.id
        elif event.chosen_inline_result:
            user_id = event.chosen_inline_result.from_user.id

        logging.info(f"User {user_id} -> Event {event}")
        return await handler(event, data)
