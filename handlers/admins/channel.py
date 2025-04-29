from aiogram import types, F, html
from loader import bot, dp, db
from states.my_state import ChannelAdd, ChannelDelete
from filters.admin_bot import IsBotAdmin as IsAdmin
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from keyboards.default.buttons import admin_button, delete_channel_verify, DeleteChannelCallback

def get_before_url():
    btn = ReplyKeyboardBuilder()
    btn.button(text="↩️ Bekor qilish")
    return btn.as_markup(resize_keyboard=True, one_time_keyboard=True)

def get_before_url_back():
    btn = ReplyKeyboardBuilder()
    btn.button(text="↩️ Orqaga")
    return btn.as_markup(resize_keyboard=True, one_time_keyboard=True)

@dp.message(F.text == "↩️ Bekor qilish")
async def get_check_and_finish(msg: types.Message, state: FSMContext):
    await state.clear()
    await msg.answer(text="⚙️ Admin Panel", reply_markup=admin_button())

@dp.message(F.text == "↩️ Orqaga")
async def get_check_and_finish(msg: types.Message, state: FSMContext):
    await state.clear()
    await msg.answer(text="⚙️ Admin Panel", reply_markup=admin_button())



@dp.message(F.text == "➕  Kanal qo\'shish", IsAdmin())
async def start_channel_add(msg: types.Message, state: FSMContext):
    await msg.answer(text="Kanal ID sini kiriting (Masalan: `-1001234567890`)", parse_mode="Markdown", reply_markup=get_before_url())
    await state.set_state(ChannelAdd.start)

@dp.message(ChannelAdd.start, IsAdmin())
async def get_id(msg: types.Message, state: FSMContext):
    channel_id = msg.text.strip()

    if not channel_id.lstrip("-").isdigit():
        await msg.answer(text="❌ Noto‘g‘ri ID! Kanal ID faqat raqamlardan iborat bo‘lishi kerak.", reply_markup=get_before_url())
        return

    if not channel_id.startswith("-"):
        await msg.answer(text="❌ Noto‘g‘ri ID! Telegram kanal ID `-100...` shaklida bo‘lishi kerak.", reply_markup=get_before_url())
        return

    if db.select_channel(channel_id=channel_id):
        await msg.answer(text="⚠️ Bu kanal allaqachon bazada mavjud!", reply_markup=get_before_url())
        await state.clear()
        return

    db.add_channel(channel_id=channel_id)
    await msg.answer(text="✅ Kanal muvaffaqiyatli qo‘shildi!", reply_markup=admin_button())
    await state.clear()

@dp.message(F.text == "♾️ Kanallar", IsAdmin())
async def start_channel_add(msg: types.Message):
    channels = db.select_all_channels()
    print(channels, "channels")
    text = ""

    for channel in channels:
        channel_id = int(channel[1])
        try:
            chat = await bot.get_chat(channel_id)
            channel_name = chat.title
            text += f"ID: {channel[0]}, CHANNEL_ID: {channel[1]}, NAME: {channel_name}\n\n"
        except Exception as e:
            print(f"Error for channel {channel[1]}: {e}")
            text += f"ID: {channel[0]}, CHANNEL_ID: {channel[1]}, NAME: Noma'lum (xato)\n\n"

    if text:
        await msg.answer(text=text, reply_markup=get_before_url_back())
    else:
        await msg.answer(text="Qo'shilgan kanallar yo'q", reply_markup=get_before_url_back())


@dp.message(F.text == "✖️ Kanal o\'chirish", IsAdmin())
async def delete_channel_id_in_database(msg: types.Message, state: FSMContext):
    await msg.answer(text="Kanalni o'chirish uchun ID yoki CHANNEL ID ni kiriting:", reply_markup=get_before_url())
    await state.set_state(ChannelDelete.start)


@dp.message(ChannelDelete.start, IsAdmin())
async def get_delete_data(msg: types.Message, state: FSMContext):
    if msg.content_type != 'text':
        await msg.answer(text="⚠️  ID yoki CHANNEL ID Kiriting!", reply_markup=get_before_url())
        return

    channel_id = msg.text.strip()

    data = db.select_channel(channel_id=channel_id)
    if not data:
        data = db.select_channel(id=channel_id)
    if not data:
        await msg.answer(text="❌ Noto‘g‘ri ID Bazada mavjud emas!", reply_markup=admin_button())
        await state.set_state(ChannelDelete.start)
        return

    try:
        chat = await bot.get_chat(channel_id)
        channel_name = chat.title
        text = f"ID: {data[0]}, CHANNEL_ID: {data[1]}, NAME: {channel_name}\n"
        await msg.answer(text, reply_markup=delete_channel_verify())
        await state.update_data({'channel_id': data[1]})
        await state.set_state(ChannelDelete.finish)
    except Exception as e:
        print(e)
        text = f"ID: {data[0]}, CHANNEL_ID: {data[1]}, NAME: Noma'lum\n"
        await msg.answer(text, reply_markup=delete_channel_verify())
        await state.update_data({'channel_id': data[1]})
        await state.set_state(ChannelDelete.finish)


@dp.callback_query(DeleteChannelCallback.filter(), ChannelDelete.finish, IsAdmin())
async def check_delete(call: types.CallbackQuery, callback_data: DeleteChannelCallback, state: FSMContext):
    await call.answer(cache_time=60)
    if callback_data.check:
        data = await state.get_data()
        db.channel_delete(data['channel_id'])
        await call.message.answer(text="✅ Kanal muvafaqiyatli o'chirildi")
        await call.message.answer(text="⚙️ Admin Panel", reply_markup=admin_button())

        await state.clear()
        return
    await state.clear()
    await call.message.answer(text="❌ O'chirish bekor qilindi")
    await call.message.answer(text="⚙️ Admin Panel", reply_markup=admin_button())




