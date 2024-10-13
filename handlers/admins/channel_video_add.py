import random
from loader import bot, dp, db
from aiogram import types, F
from filters.admin_bot import IsBotAdmin
from data.config import KINO_CHANNEL
from states.my_state import VideoChannelSend, VideoChannelSerialSend, VideoChannelSerialSendExist
from aiogram.fsm.context import FSMContext
from keyboards.inline.buttons import ChooseCallBackData, choose_button, back

@dp.message(F.text == "🎦 Kino qo'shish", IsBotAdmin())
async def get_start(message: types.Message, state: FSMContext):
    await message.answer(text="Kinoni yubroring")
    await state.set_state(VideoChannelSend.start)

@dp.message(F.video, IsBotAdmin(), VideoChannelSend.start)
async def get_caption(message: types.Message, state: FSMContext):
    video_path = message.video.file_id
    await state.update_data({
        'video_path': video_path
    })
    await state.set_state(VideoChannelSend.caption)
    await message.answer("Kinoga caption yuboring")

@dp.message(F.text, IsBotAdmin(), VideoChannelSend.caption)
async def send_video(message: types.Message, state: FSMContext):
    caption = message.text
    data = await state.get_data()
    sent_message = await bot.send_video(chat_id=KINO_CHANNEL[0], video=data['video_path'], caption=caption)
    post_id = sent_message.message_id
    await bot.send_message(chat_id=message.from_user.id, text=f"Kino muvaffaqiyatli Jo'natilindi\n"
                                                              f"Kino kodi:  {post_id}")
    await state.clear()

@dp.message(F.text == "🎦 Serial qo'shish", IsBotAdmin())
async def start_serial(message: types.Message):
    await message.answer(text="Tanlang", reply_markup=choose_button())


@dp.callback_query(ChooseCallBackData.filter(), IsBotAdmin())
async def cinema_type(call: types.CallbackQuery, callback_data: ChooseCallBackData, state: FSMContext):
    await call.answer(cache_time=60)
    cinema_type = callback_data.boolean
    if cinema_type:
        await call.message.answer(text="Post ID ni kiriting")
        await state.set_state(VideoChannelSerialSendExist.post_id)
    else:
        await call.message.answer(text="Serialni yuboring")
        await state.set_state(VideoChannelSerialSend.start)

# Serial
@dp.message(F.video, VideoChannelSerialSend.start, IsBotAdmin())
async def get_video(message: types.Message, state: FSMContext):
    video_path = message.video.file_id
    await state.update_data({
        'video_path': video_path
    })
    await message.answer("Kinoga caption yuboring")
    await state.set_state(VideoChannelSerialSend.caption)

@dp.message(F.text, IsBotAdmin(), VideoChannelSerialSend.caption, IsBotAdmin())
async def send_video(message: types.Message, state: FSMContext):
    caption = message.text
    data = await state.get_data()
    sent_message = await bot.send_video(chat_id=KINO_CHANNEL[0], video=data['video_path'], caption=caption)
    post_id = sent_message.message_id
    await bot.send_message(chat_id=message.from_user.id, text=f"Kino muvaffaqiyatli Jo'natilindi\n"
                                                              f"Kino kodi:  {post_id}")
    try:
        db.add_cinema(id=random.randint(1,1000000000000), post_id=post_id, main_id=post_id)
    except Exception as e:
        print(e)
    await state.clear()

# exists

@dp.message(F.text, VideoChannelSerialSendExist.post_id)
async def get_video(message: types.Message, state: FSMContext):
    post_id = message.text
    if not db.select_cinema(post_id=post_id):
        await message.answer(text="Serial Topilmadi", reply_markup=back())
        await state.clear()
    await message.answer(text="Serialni yuboring")
    await state.update_data({
        'post_id': post_id
    })
    await state.set_state(VideoChannelSerialSendExist.start)


@dp.message(F.video, VideoChannelSerialSendExist.start)
async def get_video(message: types.Message, state: FSMContext):
    video_path = message.video.file_id
    await state.update_data({
        'video_path': video_path
    })
    await message.answer("Kinoga caption yuboring")
    await state.set_state(VideoChannelSerialSendExist.caption)

@dp.message(F.text, IsBotAdmin(), VideoChannelSerialSendExist.caption)
async def send_video(message: types.Message, state: FSMContext):
    caption = message.text
    data = await state.get_data()
    sent_message = await bot.send_video(chat_id=KINO_CHANNEL[0], video=data['video_path'], caption=caption)
    post_id = sent_message.message_id
    await bot.send_message(chat_id=message.from_user.id, text=f"Kino muvaffaqiyatli Jo'natilindi\n"
                                                              f"Kino kodi:  {post_id}")
    try:
        db.add_cinema(id=random.randint(1,1000000000000), post_id=post_id, main_id=data['post_id'])
    except Exception as e:
        print(e)
    await state.clear()
