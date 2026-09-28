from datetime import datetime, timezone

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from keyboards.inline import get_inline_actions_kb, get_toggle_kb

router = Router()


@router.message(Command("toggle"))
async def cmd_toggle(message: Message):
    kb = get_toggle_kb(True)

    await message.answer("Включено", reply_markup=kb)


@router.message(Command("inline"))
async def cmd_inline(message: Message):
    await message.answer(
        "Выбери действие",
        reply_markup=get_inline_actions_kb(),
    )


@router.callback_query(F.data.startswith("toggle:"))
async def cb_toggle_flag(callback: CallbackQuery):
    flag = callback.data.split(":")[1] == "on"
    text = "Включено" if flag else "Выключено"

    new_kb = get_toggle_kb(flag)
    await callback.message.edit_text(text, reply_markup=new_kb)

    await callback.answer("Успешно")


@router.callback_query(F.data == "show_time")
async def cb_show_time(callback: CallbackQuery):
    await callback.message.edit_text(f"Текущее время: {datetime.now(timezone.utc)}")
    await callback.answer("Подтвердите действие", show_alert=True)


@router.callback_query(F.data == "remove_msg")
async def cb_remove_msg(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()
