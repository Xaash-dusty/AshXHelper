import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

from handlers.common import router as common_router
from handlers.echo import router as echo_router
from handlers.greet import router as greet_router
from handlers.inline import router as inline_router
from handlers.menu import router as menu_router

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


dp.include_routers(greet_router, common_router, echo_router, inline_router, menu_router)


if __name__ == "__main__":
    dp.run_polling(bot)
