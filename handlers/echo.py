from aiogram import F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

router = Router()


@router.message(Command("echo"))
async def cmd_echo(message: Message, command: CommandObject):
    await message.answer(command.args or "Нет аргументов")


@router.message(F.text & ~F.text.startswith("/"))
async def on_text(message: Message):
    await message.answer(message.text)
