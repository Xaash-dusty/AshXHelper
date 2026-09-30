from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def kb_profile_menu(is_registered=True):
    builder = InlineKeyboardBuilder()

    if not is_registered:
        builder.add(
            InlineKeyboardButton(text="Зарегистрироваться", callback_data="register")
        )
    else:
        builder.add(
            InlineKeyboardButton(text="Посмотреть", callback_data="show_profile")
        )
        builder.add(
            InlineKeyboardButton(text="Редактировать", callback_data="edit_profile")
        )
        builder.add(
            InlineKeyboardButton(
                text="Удалить", callback_data="confirm_profile_deletion"
            )
        )

    builder.adjust(1)
    return builder.as_markup()


def kb_confirm_profile_deletion():
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="Да", callback_data="delete_profile"))
    builder.add(
        InlineKeyboardButton(text="Нет", callback_data="cancel_profile_deletion")
    )

    return builder.as_markup()


def kb_backlink_and_remove(come_back_btn=True):
    builder = InlineKeyboardBuilder()
    if come_back_btn:
        builder.add(
            InlineKeyboardButton(text="Назад", callback_data="back_to_profile_menu")
        )
    builder.add(InlineKeyboardButton(text="Ok", callback_data="remove_message"))

    return builder.as_markup()


def kb_edit_profile():
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="Изменить имя", callback_data="edit_name"))
    builder.add(
        InlineKeyboardButton(text="Отмена", callback_data="back_to_profile_menu")
    )

    builder.adjust(1)

    return builder.as_markup()


def kb_show_profile():
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="Посмотреть профиль", callback_data="show_profile"))

    return builder.as_markup()