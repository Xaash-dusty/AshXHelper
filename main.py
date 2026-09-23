import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("BOT_TOKEN")
if token is None:
    raise RuntimeError("BOT_TOKEN is not set")

bot = Bot(token=token)
dp = Dispatcher()


@dp.message(CommandStart())
async def greet(message: Message):
    await message.answer("Привет!")

@dp.message(Command("stop"))
async def stop_bot(message: Message):
    await message.answer("Бот завершает свою работу")
    await dp.stop_polling()

@dp.message(F.text)
async def echo(message: Message):
    await message.answer(message.text)


if __name__ == "__main__":
    dp.run_polling(bot)