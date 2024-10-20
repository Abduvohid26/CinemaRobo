from data.config import ADMINS
from aiogram.filters import BaseFilter
from aiogram import types

class IsBotAdmin(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        print(ADMINS, 's')
        return message.from_user.id in ADMINS