# middlewares/logging.py
import logging
from aiogram import BaseMiddleware

class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user_id = None

        if getattr(event, "message", None):
            user_id = event.message.from_user.id
            event_info = event.message.text or str(event.message)
        elif getattr(event, "callback_query", None):
            user_id = event.callback_query.from_user.id
            event_info = event.callback_query.data
        elif getattr(event, "inline_query", None):
            user_id = event.inline_query.from_user.id
            event_info = event.inline_query.query
        elif getattr(event, "chosen_inline_result", None):
            user_id = event.chosen_inline_result.from_user.id
            event_info = str(event.chosen_inline_result)

        logging.info(f"User {user_id} -> Event: {event_info}")
        return await handler(event, data)
