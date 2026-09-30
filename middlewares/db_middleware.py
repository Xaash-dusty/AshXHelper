from collections.abc import Awaitable, Callable
from typing import Any

import aiogram.types
from aiogram import BaseMiddleware


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, db):
        self.db = db
        super().__init__()

    async def __call__(
        self,
        handler: Callable[
            [aiogram.types.TelegramObject, dict[str, Any]], Awaitable[Any]
        ],
        event: aiogram.types.TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        data["db"] = self.db

        return await handler(event, data)
