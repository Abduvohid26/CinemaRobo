from loader import dp, bot, db
from filters.admin_bot import IsBotAdmin
from aiogram import F, types
from aiogram.filters import Command
from keyboards.default.buttons import admin_button, rek_types
from aiogram import types

@dp.message(Command('admin'), IsBotAdmin())
async def admin(message: types.Message):
    await message.answer('Admin Panel', reply_markup=admin_button())



@dp.message(F.text == '👤 Obunachilar soni')
async def users_count(message: types.Message):
    data = db.select_all_users()
    await message.answer(f"Botdagi faol foydalanuvchilar soni {len(data)} ta.")


@dp.message(F.text == '📲 Reklama Yuborish')
async def rek_bot(message: types.Message):
    await message.answer('📲  Reklama yubiorish turini tanlang:', reply_markup=rek_types())
