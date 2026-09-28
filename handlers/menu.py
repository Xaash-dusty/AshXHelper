from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.reply import get_menu_kb

router = Router()


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer(
        "Выбери пункт из меню ниже",
        reply_markup=get_menu_kb(placeholder="Выбор за тобой..."),
    )


@router.message(F.text.in_({"Помощь", "О боте", "Закрыть"}))
async def on_reply_button(message: Message):
    if message.text == "Помощь":
        await message.answer("Команда /help для вызова помощи")
    elif message.text == "О боте":
        await message.answer("Я бот AshXHelper. Рад помочь")
    elif message.text == "Закрыть":
        await message.answer("Кнопки удалены", reply_markup=ReplyKeyboardRemove())
