from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.types import CallbackQuery, Message
from aiosqlite import Connection

from database.users import delete_user, get_user, is_user_exists
from keyboards.inline import (
    kb_backlink_and_remove,
    kb_confirm_profile_deletion,
    kb_profile_menu,
)

router = Router()


@router.message(Command("profile"), StateFilter(None))
@router.callback_query(F.data == "back_to_profile_menu", StateFilter(None))
async def cmd_profile_menu(event: Message | CallbackQuery, db: Connection):
    is_message = isinstance(event, Message)
    is_registered = await is_user_exists(db=db, user_id=event.from_user.id)
    if is_message:
        await event.answer(
            "Выбери действие", reply_markup=kb_profile_menu(is_registered)
        )
    else:
        await event.answer()
        await event.message.edit_text(
            "Выбери действие", reply_markup=kb_profile_menu(is_registered)
        )


@router.callback_query(F.data == "remove_message")
async def cb_remove_msg(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()


@router.message(Command("myself"))
@router.callback_query(F.data == "show_profile")
async def cmd_show_profile(event: Message | CallbackQuery, db: Connection):
    is_message = isinstance(event, Message)
    user = await get_user(db=db, user_id=event.from_user.id)
    if user is None:
        await event.answer("Вы не зарегистрированы")
        return

    user_id = user["user_id"]
    username = user["username"]
    name = user["name"]
    text = f"------------Profile-----------\nId: {user_id}\nUsername: {username}\nName: {name}"

    if is_message:
        await event.answer(
            text, reply_markup=kb_backlink_and_remove(come_back_btn=False)
        )
    else:
        await event.message.edit_text(text, reply_markup=kb_backlink_and_remove())
        await event.answer()


@router.callback_query(F.data == "confirm_profile_deletion")
async def cb_confirm_profile_deletion(callback: CallbackQuery):
    await callback.message.edit_text(
        "Вы уверены что хотите удалить профиль?",
        reply_markup=kb_confirm_profile_deletion(),
    )
    await callback.answer()


@router.callback_query(F.data == "cancel_profile_deletion")
async def cb_cancel_profile_deletion(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "Удаление отменено", reply_markup=kb_backlink_and_remove()
    )


@router.callback_query(F.data == "delete_profile")
async def cb_delete_profile(callback: CallbackQuery, db: Connection):
    is_deleted = await delete_user(db=db, user_id=callback.from_user.id)
    if not is_deleted:
        await callback.answer("Вы не зарегистрированы")
        return

    await callback.message.edit_text(
        "Профиль успешно удален", reply_markup=kb_backlink_and_remove()
    )
    await callback.answer()
