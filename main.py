import asyncio
import os

import aiosqlite
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

from database.users import init_db
from handlers.common import router as common_router
from handlers.editing_profile import router as editing_profile_router
from handlers.fallbacks import router as fallbacks_router
from handlers.profile import router as profile_router
from handlers.registration import router as registration_router
from middlewares.db_middleware import DatabaseMiddleware

load_dotenv()
token = os.getenv("BOT_TOKEN")
if token is None:
    raise RuntimeError("BOT_TOKEN is not set")

bot = Bot(token=token)
dp = Dispatcher()


@dp.message(Command("stop"))
async def cmd_stop(message: Message):
    await message.answer("Бот завершает свою работу")
    await dp.stop_polling()


async def main():
    dp.include_routers(
        common_router,
        registration_router,
        editing_profile_router,
        profile_router,
        fallbacks_router,
    )
    async with aiosqlite.connect("data/users.db") as db:
        db.row_factory = aiosqlite.Row
        await init_db(db)
        dp.message.middleware(DatabaseMiddleware(db))
        dp.callback_query.middleware(DatabaseMiddleware(db))

        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
