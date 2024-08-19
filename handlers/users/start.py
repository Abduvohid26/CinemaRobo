from aiogram.filters import CommandStart
from loader import dp, db, bot
from aiogram import types, F, html, suppress
from keyboards.inline.buttons import buttons
from uuid import uuid4
from utils.misc.subscription import checksubscription
from middlewares.my_middleware import CheckSubCallback
from data.config import CHANNELS
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.exceptions import TelegramBadRequest


@dp.message(CommandStart())
async def start_bot(message: types.Message):
    try:
        if db.select_user(id=message.from_user.id):
            pass
        else:
            db.add_user(id=message.from_user.id, fullname=message.from_user.full_name, telegram_id=message.from_user.id,
                        language=message.from_user.language_code)
    except Exception as e:
        print(f'Nimadur xato ketti: {e}')

    await message.answer(f"Assalomu alaykum {message.from_user.full_name}!\n\n"
                         f"✍🏻 Kino kodini yuboring.")


@dp.message(lambda message: message.text.isdigit())
async def get_cinema_number(message: types.Message):
    number = message.text
    try:
        await bot.copy_message(chat_id=message.chat.id, from_chat_id="@testcuhun", message_id=number,
                               reply_markup=buttons(film_id=number))
    except Exception as e:
        print(f'Nimadur xato ketti: {e}')
        await message.answer(' ❌ Kino kod no\'tog\'ri')


@dp.callback_query(lambda query: query.data.startswith('delete'))
async def delete_msg(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.message.chat.id, text=f'✍🏻 Kino kodini yuboring.')


@dp.message(F.text)
async def start_bot(message: types.Message):
    await message.answer(html.bold(f'👋 Assalomu alaykum {html.link(value=message.from_user.full_name, link="")} botimizga xush kelibsiz.\n\n'
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
async def check_query(call:types.CallbackQuery):
    print('Working')
    await call.answer(cache_time=60)
    user = call.from_user
    final_status = True
    btn = InlineKeyboardBuilder()
    if CHANNELS:
        for channel in CHANNELS:
            status = True
            try:
                status = await checksubscription(user_id=user.id, channel=channel)
            except Exception as e:
                print(e)
                pass
            final_status *= status
            try:
                chat = await bot.get_chat(chat_id=channel)
                if status:
                    btn.button(text=f"✅ {chat.title}", url=f"{await chat.export_invite_link()}")
                else:
                    btn.button(text=f"❌ {chat.title}", url=f"{await chat.export_invite_link()}")
            except Exception as e:
                print(e)
                pass
        if final_status:
            await call.message.answer(
                "Siz hamma kanalga a'zo bo'lgansiz!"
            )
        else:

            btn.button(
                text="🔄 Tekshirish",
                callback_data=CheckSubCallback(check=False)
            )
            btn.adjust(1)
            with suppress(TelegramBadRequest):
                await call.message.edit_text("Iltimos bot to'liq ishlashi uchun quyidagi kanal(lar)ga obuna bo'ling!",
                                             reply_markup=btn.as_markup())
    else:
        await call.message.answer(
            "Siz hamma kanalga a'zo bo'lgansiz!"
        )