

from aiogram import BaseMiddleware
from aiogram.types import Update
from typing import Callable, Awaitable, Dict, Any
import json
from loader import db
from check_url import get_data
from data.config import ADMINS

class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        from_user = event.from_user
        try:
            if db.select_user(telegram_id=from_user.id):
                pass
            else:
                db.add_user(fullname=from_user.full_name, telegram_id=from_user.id,
                            language=from_user.language_code)
                await get_data(chat_id=ADMINS[0])
                
        except Exception as e:
            print(f'Nimadur xato ketti: {e}')
        return await handler(event, data)