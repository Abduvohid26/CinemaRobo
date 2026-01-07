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
    user = call.from_user
    final_status = True
    btn = InlineKeyboardBuilder()

    # 1. Barcha kanallarni bitta ro'yxatga yig'amiz
    all_channels = list(CHANNELS_STATIC) # Static kanallar
    db_channels = db.select_all_channels()
    if db_channels:
        for ch in db_channels:
            # Bazadagi kanal ID yoki username oxirgi elementda deb hisobladik: ch[-1]
            if ch[-1] not in all_channels:
                all_channels.append(ch[-1])

    # 2. Har bir kanalni tekshiramiz
    for channel_id in all_channels:
        try:
            # Obunani tekshirish
            status = await checksubscription(user_id=user.id, channel=channel_id)
            final_status = final_status and status
            
            # Kanal ma'lumotlarini olish
            chat = await bot.get_chat(chat_id=channel_id)
            
            # Havola yaratish: Agar username bo'lsa t.me/link, bo'lmasa invite_link
            if chat.username:
                invite_link = f"https://t.me/{chat.username}"
            else:
                # Private kanallar uchun (bot admin bo'lishi kerak)
                invite_link = chat.invite_link
                if not invite_link:
                    invite_link = await chat.export_invite_link()

            btn.button(
                text=f"{'✅' if status else '❌'} {chat.title}",
                url=invite_link
            )
        except Exception as e:
            print(f"Xatolik: {channel_id} kanalini tekshirishda: {e}")
            continue # Xato bo'lsa keyingi kanalga o'tish

    # 3. Natijani tekshirish
    if final_status:
        await call.message.delete()
        if not db.select_user(telegram_id=user.id):
            db.add_user(
                fullname=user.full_name, 
                telegram_id=user.id,
                language=user.language_code
            )
            # Admin xabarnomasi (ixtiyoriy)
            # await get_data(chat_id=ADMINS[0]) 

        await call.message.answer(
            text=f"👋 Assalomu alaykum {html.link(user.full_name, f'tg://user?id={user.id}')} botimizga xush kelibsiz.\n\n"
                 f"✍🏻 Kino kodini yuboring",
            parse_mode="HTML"
        )
    else:
        # Obuna bo'lmagan bo'lsa tugmani chiqarish
        btn.button(text="🔄 Tekshirish", callback_data=CheckSubCallback(check=False))
        btn.adjust(1)
        
        # Xabar matnini yangilash yoki qayta yuborish
        text = ("🔔 <b>Davom etish uchun barcha kanallarga obuna bo‘ling!</b>\n\n"
                "❗️ Obuna bo‘lgach 'Tekshirish' tugmasini bosing.")
        
        # Har safar yangi xabar yubormaslik uchun edit qilamiz
        try:
            await call.message.edit_text(text=text, reply_markup=btn.as_markup(), parse_mode="HTML")
        except:
            # Agar xabar o'zgarmagan bo'lsa edit_text xato beradi
            pass