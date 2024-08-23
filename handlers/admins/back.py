# from loader import bot, dp
# from aiogram import F, types
# from filters.admin_bot import IsBotAdmin
# from keyboards.default.buttons import admin_button, rek_types
#
# @dp.message(F.text == '🔙 Orqaga', IsBotAdmin())
# async def render_admin_panel(message: types.Message):
#     await message.answer('Admin Panel', reply_markup=admin_button())
#
#
# @dp.message(F.text == '📌 Bekor qilish', IsBotAdmin())
# async def render_rek_type_panel(message: types.Message):
#     await message.answer('📲  Reklama yubiorish turini tanlang:', reply_markup=rek_types())