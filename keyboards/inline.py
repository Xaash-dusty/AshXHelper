from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_toggle_kb(is_enabled: bool):
    builder = InlineKeyboardBuilder()

    text = "Выключить" if is_enabled else "Включить"
    callback = "toggle:off" if is_enabled else "toggle:on"

    builder.add(InlineKeyboardButton(text=text, callback_data=callback))
    return builder.as_markup()


def get_inline_actions_kb():
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="Показать время", callback_data="show_time"))
    builder.add(
        InlineKeyboardButton(text="Удалить сообщение", callback_data="remove_msg")
    )
    builder.adjust(1)
    return builder.as_markup()
