# services/relay.py
from db.database import get_pair_by_user

async def relay_message(bot, sender_id: int, message):
    pair = await get_pair_by_user(sender_id)
    if not pair:
        return

    target = pair["receiver_id"] if sender_id == pair["giver_id"] else pair["giver_id"]

    await bot.copy_message(
        chat_id=target,
        from_chat_id=message.chat.id,
        message_id=message.message_id
    )
