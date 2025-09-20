import aiosqlite
import asyncio

query_older = "SELECT * FROM users WHERE age > ?"
query_all = "SELECT * FROM users"
db_name = 'users.db'
param = 40


async def async_fetch_users():
    async with aiosqlite.connect(db_name) as db:
        async with db.execute(query_all) as cursor:
            rows = await cursor.fetchall()
            return rows


async def async_fetch_older_users():
    async with aiosqlite.connect(db_name) as db:
        async with db.execute(query_older, (param,)) as cursor:
            rows = await cursor.fetchall()
            return rows


async def fetch_concurrently():
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("👥 All users:", all_users)
    print(f"👴 Users older than {param}:", older_users)


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
