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
            receiver_id INTEGER
        )
        """)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS tracks (
            receiver_id INTEGER,
            track TEXT
        )
        """)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_id INTEGER,
            to_id INTEGER,
            role TEXT,        -- 'santa' или 'receiver'
            message_type TEXT, -- text, photo, document, sticker
            content TEXT,
            file_id TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
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
        await db.executemany("INSERT INTO pairs VALUES (?,?)", pairs)
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

async def save_track_number(receiver_id: int, track: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT INTO tracks VALUES (?,?)", (receiver_id, track))
        await db.commit()

# Функция сохранения сообщения
async def save_chat_message(from_id: int, to_id: int, role: str, message_type: str, content: str, file_id: str | None = None):
    """
    Сохраняет сообщение в чат.
    from_id: кто отправил
    to_id: кто получил
    role: 'santa' или 'receiver'
    message_type: 'text', 'photo', 'document' и т.д.
    content: текст сообщения или подпись
    file_id: для медиа (фото, файл)
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            INSERT INTO chat_messages (from_id, to_id, role, message_type, content, file_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (from_id, to_id, role, message_type, content, file_id)
        )
        await db.commit()


async def get_chat_history(user_id: int, role: str):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("""
            SELECT from_id, message_type, content, file_id
            FROM chat_messages
            WHERE to_id = ? AND role = ?
            ORDER BY created_at
        """, (user_id, role))
        rows = await cur.fetchall()

    return [
        {
            "from_id": r[0],
            "message_type": r[1],
            "content": r[2],
            "file_id": r[3],
        }
        for r in rows
    ]

async def get_pair_for_user(user_id: int, role: str):
    """
    Возвращает пару для пользователя.
    role: 'santa' или 'receiver'
    """
    async with aiosqlite.connect(DB_PATH) as db:
        if role == "santa":
            # user_id — Санта, ищем его получателя
            cur = await db.execute(
                "SELECT receiver_id FROM pairs WHERE giver_id=?", (user_id,)
            )
            row = await cur.fetchone()
            if row:
                return {"receiver_id": row[0]}
        elif role == "receiver":
            # user_id — Получатель, ищем его Санту
            cur = await db.execute(
                "SELECT giver_id FROM pairs WHERE receiver_id=?", (user_id,)
            )
            row = await cur.fetchone()
            if row:
                return {"giver_id": row[0]}
    return None

async def check_distributed() -> bool:
    """Проверяет, были ли распределены пары (есть ли записи в таблице pairs)."""
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT COUNT(*) FROM pairs")
        count = (await cur.fetchone())[0]
    return count > 0
