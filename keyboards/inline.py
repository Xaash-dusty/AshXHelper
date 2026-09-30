from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def kb_profile_menu():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text="Зарегестрироваться", callback_data="register")
    )
    builder.add(InlineKeyboardButton(text="Посмотреть", callback_data="show profile"))
    builder.add(
        InlineKeyboardButton(text="Редактировать", callback_data="edit profile")
    )
    builder.add(InlineKeyboardButton(text="Удалить", callback_data="delete profile"))

    builder.adjust(1)
    return builder.as_markup()


def kb_profile_info():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Назад", callback_data="back to profile menu")
    )
    builder.add(
        InlineKeyboardButton(text="Удалить сообщение", callback_data="remove message")
    )

    return builder.as_markup()


def kb_edit_profile():
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="Изменить имя", callback_data="edit name"))
    builder.add(
        InlineKeyboardButton(text="Отмена", callback_data="back to profile menu")
    )

    builder.adjust(1)

    return builder.as_markup()
