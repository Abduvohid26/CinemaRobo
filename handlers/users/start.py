from aiogram.filters import CommandStart

from filters import IsBotAdmin
from loader import dp, db, bot
from aiogram import types, F, html, suppress
from keyboards.inline.buttons import buttons
from uuid import uuid4
from utils.misc.subscription import checksubscription
from middlewares.my_middleware import CheckSubCallback
from data.config import ADMINS
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio
from aiogram.utils.keyboard import InlineKeyboardBuilder
from check_url import get_data
from data.config import KINO_CHANNEL
from aiogram.types import Update
import logging
from aiogram import html

logger = logging.getLogger(__name__)


@dp.message(CommandStart())
async def start_bot(message: types.Message):
    # try:
    #     if db.select_user(telegram_id=message.from_user.id):
    #         pass
    #     else:
    #         db.add_user(fullname=message.from_user.full_name, telegram_id=message.from_user.id,
    #                     language=message.from_user.language_code)
    #         await get_data(chat_id=ADMINS[0])

            
    # except Exception as e:
    #     print(f'Nimadur xato ketti: {e}')

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
            await bot.copy_message(chat_id=message.chat.id, from_chat_id=f"{KINO_CHANNEL[0]}", message_id=number,
                                   reply_markup=buttons(film_id=number), protect_content=True)
            
        await bot.send_message(
                chat_id=message.chat.id,
                text=(
                    "🎥 Videolarni sifatli va tekin yuklang!\n"
                    "⚡️ Instagram, TikTok, Facebook — hammasi bittada.\n"
                    "📥 Manzil: https://voltsaver.top"
                )
            )
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


CHANNELS_STATIC = ['@abduvohiddev', '@Xabarnomada', '@Lidernoma', '@Biznes_savodxonlik']

@dp.callback_query(CheckSubCallback.filter())
async def check_query(call: types.CallbackQuery):
    await call.answer(cache_time=0)
    user_id = call.from_user.id
    final_status = True
    btn = InlineKeyboardBuilder()

    CHANNELS = db.select_all_channels()
    
    if CHANNELS:
        for channel in CHANNELS:
            channel_id = channel[-1] 
            try:
                # Obunani tekshirish
                status = await checksubscription(user_id=user_id, channel=channel_id)
                
                if not status:
                    # Agar obuna bo'lmagan bo'lsa, final_status ni False qilamiz
                    final_status = False
                    
                    # Kanal ma'lumotlarini olish
                    chat = await bot.get_chat(chat_id=channel_id)
                    
                    if chat.username:
                        invite_link = f"https://t.me/{chat.username}"
                    else:
                        invite_link = chat.invite_link or await chat.export_invite_link()

                    # Faqat obuna bo'lmagan kanalni tugmaga qo'shamiz
                    btn.button(
                        text=f"❌ {chat.title}",
                        url=invite_link
                    )
            except Exception as e:
                print(f"Kanalda xatolik ({channel_id}): {e}")

        if final_status:
            # Hammasiga obuna bo'lgan bo'lsa
            await call.message.delete()
            
            # Bazaga qo'shish (agar yo'q bo'lsa)
            if not db.select_user(telegram_id=user_id):
                db.add_user(
                    fullname=call.from_user.full_name, 
                    telegram_id=user_id,
                    language=call.from_user.language_code
                )
                # Admin xabar berish (agar kerak bo'lsa)
                # await get_data(chat_id=ADMINS[0]) 

            # Siz aytgan chiroyli matnli xabar
            text = html.bold(
                f'👋 Assalomu alaykum {html.link(value=call.from_user.full_name, link=f"tg://user?id={user_id}")} '
                f'botimizga xush kelibsiz.\n\n'
                f'✍🏻 Kino kodini yuboring'
            )
            await call.message.answer(text)
            
        else:
            # Hali obuna bo'lmagan kanallari bo'lsa
            btn.button(text="🔄 Tekshirish", callback_data=CheckSubCallback(check=False))
            btn.adjust(1)
            
            # Faqat markupni yangilaymiz (xabar matni o'zgarmaydi, tugmalar kamayadi)
            try:
                await call.message.edit_reply_markup(reply_markup=btn.as_markup())
            except:
                # Agar markup o'zgarmagan bo'lsa (masalan, hali ham o'sha kanallar) xato bermasligi uchun
                pass
    else:
        # Agar bazada kanallar bo'lmasa, to'g'ridan-to'g'ri kirgazish
        await call.message.delete()
        text = html.bold(
            f'👋 Assalomu alaykum {html.link(value=call.from_user.full_name, link=f"tg://user?id={user_id}")} '
            f'botimizga xush kelibsiz.\n\n'
            f'✍🏻 Kino kodini yuboring'
        )
        await call.message.answer(text)

# @dp.callback_query(CheckSubCallback.filter())
# async def check_query(call: types.CallbackQuery):
#     await call.answer(cache_time=0)
#     user = call.from_user
#     final_status = True
#     btn = InlineKeyboardBuilder()

#     await call.message.delete()
#     CHANNELS = db.select_all_channels()
#     if CHANNELS:
#         for channel in CHANNELS:
#             try:
#                 status = await checksubscription(user_id=user.id, channel=channel[-1])
#                 final_status = final_status and status
#                 chat = await bot.get_chat(chat_id=channel[-1])
#                 invite_link = await chat.export_invite_link()  
#                 btn.button(
#                     text=f"{'✅' if status else '❌'} {chat.title}",
#                     url=invite_link
#                 )
#             except Exception as e:
#                 print(f"Kanalga kirish yoki linkni olishda xato: {e}")

#         if final_status:
#             if not db.select_user(telegram_id=call.message.from_user.id):
#                 db.add_user(fullname=call.message.from_user.full_name, telegram_id=call.message.from_user.id,
#                             language=call.message.from_user.language_code)
#                 await get_data(chat_id=ADMINS[0])

                
#             await call.message.answer(html.bold(f'👋 Assalomu alaykum {html.link(value=call.message.from_user.full_name, link=f"tg://user?id={call.message.from_user.id}")} botimizga xush kelibsiz.\n\n'
#                                    f'✍🏻 Kino kodini yuboring'))
#             return
#         else:
#             btn.button(
#                 text="🔄 Tekshirish",
#                 callback_data=CheckSubCallback(check=False)
#             )
#             btn.adjust(1)
#             await call.message.answer(
#                 text=(
#                     "🔔 *Davom etish uchun barcha kanallarga obuna bo‘ling!*\n\n"
#                     "❗️ Agar obuna bo‘lishda xatolik yuz bergan bo‘lsa, "
#                     "*/start* buyrug‘ini qayta bosib, yana urinib ko‘ring."
#                 ),
#                 reply_markup=btn.as_markup()
#             )
#     else:
#         if not db.select_user(telegram_id=call.message.from_user.id):
#                 db.add_user(fullname=call.message.from_user.full_name, telegram_id=call.message.from_user.id,
#                             language=call.message.from_user.language_code)
#                 await get_data(chat_id=ADMINS[0])

                
#         await call.message.answer(html.bold(f'👋 Assalomu alaykum {html.link(value=call.message.from_user.full_name, link=f"tg://user?id={call.message.from_user.id}")} botimizga xush kelibsiz.\n\n'
#                                    f'✍🏻 Kino kodini yuboring'))