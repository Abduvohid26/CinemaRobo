from aiogram.filters import CommandStart

from filters import IsBotAdmin
from loader import dp, db, bot
from aiogram import types, F, html, suppress
from keyboards.inline.buttons import buttons
from uuid import uuid4
from utils.misc.subscription import checksubscription
from middlewares.my_middleware import CheckSubCallback
from data.config import CHANNELS, ADMINS
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio
from aiogram.utils.keyboard import InlineKeyboardBuilder
from check_url import get_data

@dp.message(CommandStart())
async def start_bot(message: types.Message):
    try:
        if db.select_user(id=message.from_user.id):
            pass
        else:
            await get_data(chat_id=ADMINS[0])
            db.add_user(id=message.from_user.id, fullname=message.from_user.full_name, telegram_id=message.from_user.id,
                        language=message.from_user.language_code)
    except Exception as e:
        print(f'Nimadur xato ketti: {e}')

    await message.answer(html.bold(f'👋 Assalomu alaykum {html.link(value=message.from_user.full_name, link=f"tg://user?id={message.from_user.id}")} botimizga xush kelibsiz.\n\n'
                                   f'✍🏻 Kino kodini yuboring'))

def create_serial_buttons(serials):
    btn = InlineKeyboardBuilder()
    i = 0
    for serial in serials:
        i += 1
        btn.button(text=f"Serial {i}", callback_data=f"serial_{serial[2]}")
    return btn.as_markup()

@dp.message(lambda message: message.text.isdigit())
async def get_cinema_number(message: types.Message):
    number = message.text
    try:
        serials = db.select_all_cinema(main_id=number)
        if serials:
            await message.answer(text="Quyidagi seriallar mavjud:", reply_markup=create_serial_buttons(serials))
        else:
            await bot.copy_message(chat_id=message.chat.id, from_chat_id="@testcuhun", message_id=number,
                                   reply_markup=buttons(film_id=number))
    except Exception as e:
        print(f'Nimadur xato ketti: {e}')
        await message.answer(' ❌ Kino kod no\'tog\'ri')

@dp.callback_query(lambda c: c.data and c.data.startswith("serial_"))
async def handle_serial_callback(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    serial_id = call.data.split("_")[1]
    await bot.copy_message(chat_id=call.message.chat.id, from_chat_id="@testcuhun", message_id=serial_id,
                           reply_markup=buttons(film_id=serial_id))


@dp.callback_query(lambda query: query.data.startswith('delete'))
async def delete_msg(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.message.chat.id, text=f'✍🏻 Kino kodini yuboring.')


@dp.message(F.text)
async def start_bot(message: types.Message):
    await message.answer(html.bold(f'👋 Assalomu alaykum {html.link(value=message.from_user.full_name, link=f"tg://user?id={message.from_user.id}")} botimizga xush kelibsiz.\n\n'
                                   f'✍🏻 Kino kodini yuboring'))


@dp.inline_query()
async def inline_handler(inline_query: types.InlineQuery):
    """
    Handle inline queries and respond with video_send.py results.
    """
    try:
        film_id = int(inline_query.query)
        message_url = f"https://t.me/testcuhun/{film_id}"
        result = types.InlineQueryResultVideo(
            id=str(uuid4()),
            title="Videoni do'stlarga yuborish",
            video_url=message_url,
            description=f"ID: {film_id}",
            thumbnail_url='https://t.me/ulugbekhusain/49',
            mime_type='video_send.py/mp4',
            caption="@super_cinema_robot"
        )

        await bot.answer_inline_query(
            inline_query.id,
            results=[result],
            cache_time=10,
            is_personal=True,
            switch_pm_parameter="add",
            switch_pm_text="Botga o'tish"
        )
    except Exception as e:
        print(f"Error handling inline query: {e}")




@dp.callback_query(CheckSubCallback.filter())
async def check_query(call: types.CallbackQuery):
    await call.answer(cache_time=0)
    user = call.from_user
    final_status = True
    btn = InlineKeyboardBuilder()

    if CHANNELS:
        for channel in CHANNELS:
            try:
                status = await checksubscription(user_id=user.id, channel=channel)
                final_status = final_status and status
                chat = await bot.get_chat(chat_id=channel)
                invite_link = await chat.export_invite_link()
                btn.button(
                    text=f"{'✅' if status else '❌'} {chat.title}",
                    url=invite_link
                )
            except Exception as e:
                print(f"Kanalga kirish yoki linkni olishda xato: {e}")

        if final_status:
            await call.message.answer(f"Assalomu alaykum {call.message.from_user.full_name}!\n\n"
                         f"✍🏻 Kino kodini yuboring.")
        else:
            btn.button(
                text="🔄 Tekshirish",
                callback_data=CheckSubCallback(check=False)
            )
            btn.adjust(1)
            data = await call.message.answer(
                text="Iltimos avval barcha kanallarga azo boling !"
            )
            await asyncio.sleep(5)
            await data.delete()
    else:
        await call.message.answer(f"Assalomu alaykum {call.message.from_user.full_name}!\n\n"
                         f"✍🏻 Kino kodini yuboring.")