from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет!", reply_markup=ReplyKeyboardRemove())


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "Привет, этот бот служит для изучения библиотеки aiogram. Сейчас он использует текстовые ответы, а также reply и inline клавиатуры"
    )
