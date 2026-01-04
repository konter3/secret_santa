import random
from db.database import save_pairs, lock_profiles
import aiosqlite
from config import DB_PATH

async def distribute():
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT user_id FROM profiles")
        users = [row[0] for row in await cur.fetchall()]

    random.shuffle(users)
    pairs = [(users[i], users[(i+1) % len(users)]) for i in range(len(users))]
    await save_pairs(pairs)
    await lock_profiles()
    return pairs
