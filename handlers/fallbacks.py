from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("cancel"))
async def on_cancel_outside_state(message: Message):
    await message.answer("Нечего отменять")


@router.message(F.text.startswith("/"))
async def on_undefined_cmd(message: Message):
    await message.answer("Неизвестная команда. Для вызова справки /help")


@router.message(F.text)
async def on_undefined_text(message: Message):
    await message.answer("Я не понимаю что тебе надо")
