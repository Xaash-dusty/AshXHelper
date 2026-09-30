from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiosqlite import Connection

from database.users import edit_name, is_user_exists
from keyboards.inline import kb_backlink_and_remove, kb_edit_profile

router = Router()


class EditingName(StatesGroup):
    new_name = State()


@router.message(EditingName.new_name, Command("cancel"))
async def cmd_cancel_editing(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Редактирование профиля прервано")


@router.message(EditingName.new_name, F.text & ~F.text.startswith("/"))
async def on_new_name(message: Message, state: FSMContext, db: Connection):
    try:
        old_name = await edit_name(
            db=db, user_id=message.from_user.id, new_name=message.text
        )
        await message.answer(
            f"Имя изменено с '{old_name}' на '{message.text}'",
            reply_markup=kb_backlink_and_remove(),
        )
    except ValueError as e:
        await message.answer(str(e))

    await state.clear()


@router.message(EditingName.new_name, F.text.startswith("/"))
async def on_unavailable_cmd(messsage: Message):
    await messsage.answer(
        "Глобальные команды недоступны в режиме регистрации. Для выхода /cancel"
    )


@router.message(EditingName.new_name)
async def on_invalid_new_name(message: Message):
    await message.answer("Пришли имя текстом, например: Иван.\nВведите новое имя...")


@router.callback_query(F.data == "edit_profile")
async def cb_edit_profile(callback: CallbackQuery, db: Connection):
    if not await is_user_exists(db=db, user_id=callback.from_user.id):
        await callback.answer("Вы не зарегистрированы")
        return

    await callback.message.edit_text(
        "Выбери, что хочешь изменить", reply_markup=kb_edit_profile()
    )
    await callback.answer()


@router.callback_query(F.data == "edit_name")
async def cb_edit_name(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите новое имя...")
    await state.set_state(EditingName.new_name)
    await callback.answer()
