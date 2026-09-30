from aiosqlite import Connection, Row


async def init_db(db: Connection) -> None:
    await db.execute("""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE,
    username TEXT,
    name TEXT
    )""")
    await db.commit()


async def is_user_exists(db: Connection, user_id: int) -> bool:
    async with db.execute(
        "SELECT 1 FROM users WHERE user_id = ?", (user_id,)
    ) as cursor:
        result = await cursor.fetchone()
        return bool(result)


async def create_user(
    db: Connection, user_id: int, username: str | None, name: str | None
) -> None:
    await db.execute(
        """INSERT OR IGNORE INTO users (user_id, username, name) VALUES (?, ?, ?)""",
        (user_id, username, name),
    )
    await db.commit()


async def get_user(db: Connection, user_id: int) -> Row | None:
    async with db.execute(
        "SELECT * FROM users WHERE user_id = ?", (user_id,)
    ) as cursor:
        user = await cursor.fetchone()
        return user


async def delete_user(db: Connection, user_id: int) -> None:
    await db.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    await db.commit()


async def edit_name(db: Connection, user_id: int, new_name: str) -> dict[str, str]:
    user = await get_user(db=db, user_id=user_id)
    old_name = user["name"]
    await db.execute("UPDATE users SET name = ? WHERE user_id = ?", (new_name, user_id))
    await db.commit()
    return {"old_name": old_name, "new_name": new_name}
