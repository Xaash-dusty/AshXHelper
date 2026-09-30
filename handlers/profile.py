from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.types import CallbackQuery, Message
from aiosqlite import Connection

from database.users import delete_user, get_user, is_user_exists
from keyboards.inline import kb_profile_info, kb_profile_menu

router = Router()


@router.message(Command("profile"), StateFilter(None))
@router.callback_query(F.data == "back to profile menu", StateFilter(None))
async def cmd_profile_menu(event: Message | CallbackQuery):
    is_message = isinstance(event, Message)
    if is_message:
        await event.answer("Выбери действие", reply_markup=kb_profile_menu())
    else:
        await event.answer()
        await event.message.edit_text("Выбери действие", reply_markup=kb_profile_menu())


@router.callback_query(F.data == "remove message")
async def cb_remove_msg(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()


@router.callback_query(F.data == "show profile")
async def cb_show_profile(callback: CallbackQuery, db: Connection):
    if not await is_user_exists(db=db, user_id=callback.from_user.id):
        await callback.answer("Вы не зарегестрированы")
        return

    _, user_id, username, name = await get_user(db=db, user_id=callback.from_user.id)
    await callback.message.edit_text(
        f"------------Profile-----------\nId: {user_id}\nUsername: {username}\nName: {name}",
        reply_markup=kb_profile_info(),
    )
    await callback.answer()


@router.callback_query(F.data == "delete profile")
async def cb_delete_profile(callback: CallbackQuery, db: Connection):
    if not await is_user_exists(db=db, user_id=callback.from_user.id):
        await callback.answer("Вы не зарегестрированны")
        return

    await delete_user(db=db, user_id=callback.from_user.id)
    await callback.message.edit_text(
        "Профиль успешно удален", reply_markup=kb_profile_info()
    )
    await callback.answer()
