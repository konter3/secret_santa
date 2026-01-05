# db/database.py
import aiosqlite
from config import DB_PATH

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            wishes TEXT,
            dislikes TEXT,
            delivery TEXT,
            address TEXT,
            locked INTEGER DEFAULT 0
        )
        """)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS pairs (
            giver_id INTEGER,
            receiver_id INTEGER,
            track_number TEXT DEFAULT NULL
        )
        """)
     

        await db.commit()

async def get_profile(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT * FROM profiles WHERE user_id=?", (user_id,))
        return await cur.fetchone()

async def save_profile(data: dict):
    """
    data = {
        "user_id": ...,
        "name": ...,
        "wishes": ...,
        "dislikes": ...,
        "delivery": ...,
        "address": ...
    }
    locked будет по умолчанию 0
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT OR REPLACE INTO profiles 
            (user_id, name, wishes, dislikes, delivery, address)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data["user_id"],
            data["name"],
            data["wishes"],
            data["dislikes"],
            data["delivery"],
            data["address"]
        ))
        await db.commit()


async def delete_profile(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM profiles WHERE user_id=?", (user_id,))
        await db.commit()

async def count_profiles():
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT COUNT(*) FROM profiles")
        return (await cur.fetchone())[0]

async def lock_profiles():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE profiles SET locked=1")
        await db.commit()

async def save_pairs(pairs: list[tuple[int, int]]):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM pairs")
        await db.executemany(
            "INSERT INTO pairs (giver_id, receiver_id) VALUES (?, ?)",
            pairs
        )
        await db.commit()


async def get_pair_by_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "SELECT * FROM pairs WHERE giver_id=? OR receiver_id=?",
            (user_id, user_id)
        )
        row = await cur.fetchone()
        if not row:
            return None
        return {"giver_id": row[0], "receiver_id": row[1]}

async def get_pair_by_giver(giver_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "SELECT giver_id, receiver_id, track_number FROM pairs WHERE giver_id=?",
            (giver_id,)
        )
        row = await cur.fetchone()
        if not row:
            return None
        return {
            "giver_id": row[0],
            "receiver_id": row[1],
            "track_number": row[2]
        }

async def get_pair_by_receiver(receiver_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "SELECT giver_id, receiver_id, track_number FROM pairs WHERE receiver_id=?",
            (receiver_id,)
        )
        row = await cur.fetchone()
        if not row:
            return None
        return {
            "giver_id": row[0],
            "receiver_id": row[1],
            "track_number": row[2]
        }

async def save_track_number(giver_id: int, track: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE pairs SET track_number=? WHERE giver_id=?",
            (track, giver_id)
        )
        await db.commit()


async def check_distributed() -> bool:
    """Проверяет, были ли распределены пары (есть ли записи в таблице pairs)."""
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT COUNT(*) FROM pairs")
        count = (await cur.fetchone())[0]
    return count > 0
