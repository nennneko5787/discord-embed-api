import asyncio
import sqlite3

import aiosqlite


class DBService:
    pool: aiosqlite.Connection = None

    @classmethod
    async def init(cls):
        cls.pool: aiosqlite.Connection = await aiosqlite.connect("database.db")
        cls.pool.row_factory = sqlite3.Row

    @classmethod
    async def shutdown(cls):
        async with asyncio.timeout(10):
            await cls.pool.close()
