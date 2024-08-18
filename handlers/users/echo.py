from loader import dp
from aiogram import types,F
@dp.message(F.text)
async def echo_bot(message:types.Message):
    await message.answer(message.text)
