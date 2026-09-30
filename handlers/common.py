from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
from aiosqlite import Connection

from database.users import is_user_exists

router = Router()


@router.message(CommandStart(), StateFilter(None))
async def cmd_start(message: Message, db: Connection):
    if await is_user_exists(db=db, user_id=message.from_user.id):
        text = """
Привет! В этом боте ты можешь регистрироваться, а также изменять и смотреть свой профиль.
Для вызова справки /help
"""
    else:
        text = """
Привет! В этом боте ты можешь регистрироваться, а также изменять и смотреть свой профиль.
Для вызова справки /help
        
Может ты хочешь зарегистрироваться? /register
"""
    await message.answer(
        text,
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Command("help"), StateFilter(None))
async def cmd_help(message: Message):
    await message.answer("""
/help - Вызов данной справки
/start  - Запуск бота
/stop - Остановить бота
----------------Управление профилем------------------
/register - Начать регистрацию
/cancel - Отменить форму
/profile - Посмотреть, отредактировать или удалить профиль
/myself - Посмотреть свой профиль
    """)
