from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiosqlite import Connection

from database.users import create_user, is_user_exists
from keyboards.inline import kb_show_profile

router = Router()


class Registration(StatesGroup):
    name = State()


@router.message(Registration.name, Command("cancel"))
async def cmd_cancel_registration(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Регистрация прервана")


@router.message(Command("register"), StateFilter(None))
@router.callback_query(F.data == "register", StateFilter(None))
async def cmd_register(
    event: Message | CallbackQuery, state: FSMContext, db: Connection
):
    is_message = isinstance(event, Message)
    if await is_user_exists(db=db, user_id=event.from_user.id):
        await event.answer("Вы уже зарегистрированы")
        return

    await state.set_state(Registration.name)
    if is_message:
        await event.answer(
            "Регистрация началась, для отмены введите /cancel.\nВведите имя..."
        )
    else:
        await event.answer()
        await event.message.answer(
            "Регистрация началась. Для отмены /cancel. Введите имя..."
        )


@router.message(Registration.name, F.text & ~F.text.startswith("/"))
async def on_name(message: Message, state: FSMContext, db: Connection):
    await state.update_data(name=message.text)
    data = await state.get_data()
    await create_user(
        db=db,
        user_id=message.from_user.id,
        username=message.from_user.username,
        name=data["name"],
    )
    await message.answer(
        f"Вы зарегистрированы под именем '{data['name']}'",
        reply_markup=kb_show_profile(),
    )
    await state.clear()


@router.message(Registration.name, F.text.startswith("/"))
async def on_unavailable_cmd(message: Message):
    await message.answer(
        "Глобальные команды недоступны в режиме регистрации. Для выхода /cancel"
    )


@router.message(Registration.name)
async def on_invalid_name(message: Message):
    await message.answer("Имя должно быть строкой.\nВведите имя...")
