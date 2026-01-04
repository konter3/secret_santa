import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from db.database import init_db
from handlers import profile_edit, start, profile, admin, chat, tracking
from middlewares.chat_antispam import ChatAntiSpamMiddleware
from middlewares.logging import LoggingMiddleware

async def main():
    logging.basicConfig(level=logging.INFO)
    await init_db()

    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    dp.message.middleware(ChatAntiSpamMiddleware())
    dp.callback_query.middleware(ChatAntiSpamMiddleware())
    dp.update.middleware(LoggingMiddleware())
    dp.include_router(chat.router)
    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(profile_edit.router)
    dp.include_router(admin.router)
    
    dp.include_router(tracking.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
