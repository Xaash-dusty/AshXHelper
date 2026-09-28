from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_menu_kb(*, resize: bool = True, placeholder: str | None = None):
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Помощь"))
    builder.add(KeyboardButton(text="О боте"))
    builder.add(KeyboardButton(text="Закрыть"))
    builder.adjust(2, 1)
    return builder.as_markup(
        resize_keyboard=resize,
        input_field_placeholder=placeholder,
    )
