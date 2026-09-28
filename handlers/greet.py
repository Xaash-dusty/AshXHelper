from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

router = Router()


class Greet(StatesGroup):
    name = State()
    age = State()


@router.message(Command("cancel"), StateFilter(Greet.name, Greet.age))
@router.message(F.text.casefold() == "отмена", StateFilter(Greet.name, Greet.age))
async def cancel_greet(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Нечего отменять")
        return

    await state.clear()
    await message.answer("Приветствие прервано")


@router.message(Command("greet"))
async def cmd_greet(message: Message, state: FSMContext):
    await message.answer("Как тебя зовут?")
    await state.set_state(Greet.name)


@router.message(Greet.name, F.text)
async def on_name(message: Message, state: FSMContext):
    await state.update_data(user_name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Greet.age)


@router.message(Greet.name)
async def on_invalid_name(message: Message):
    await message.answer("Имя нужно прислать текстом")


@router.message(Greet.age, F.text.isdigit())
async def on_age(message: Message, state: FSMContext):
    await state.update_data(user_age=int(message.text))
    data = await state.get_data()

    name = data["user_name"]
    age = data["user_age"]

    await message.answer(f"Тебя зовут {name}, тебе {age} лет")

    await state.clear()


@router.message(Greet.age)
async def on_invalid_age(message: Message):
    await message.answer("Возраст должен быть числом")
