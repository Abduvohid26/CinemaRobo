from aiogram import BaseMiddleware
from aiogram.types import Message,Update
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import *
from loader import bot, db
# from data.config import CHANNELS
from utils.misc.subscription import checksubscription
from aiogram.filters.callback_data import CallbackData


class CheckSubCallback(CallbackData,prefix='check'):
    check :bool

CHANNELS_STATIC = ['@abduvohiddev', '@Xabarnomada', '@Lidernoma', '@Biznes_savodxonlik']


class UserCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        # Faqat xabarlar va callbacklar uchun ishlasin
        if not event.message and not event.callback_query:
            return await handler(event, data)

        user = event.from_user
        if not user:
            return await handler(event, data)

        CHANNELS = db.select_all_channels()
        if not CHANNELS:
            return await handler(event, data)

        final_status = True
        btn = InlineKeyboardBuilder()

        for channel in CHANNELS:
            channel_id = channel[-1]
            status = await checksubscription(user_id=user.id, channel=channel_id)
            final_status = final_status and status
            
            # Har safar get_chat qilmaslik uchun bazada kanal nomini va linkini saqlash kerak
            # Hozircha oddiyroq usul:
            if not status:
                try:
                    chat = await bot.get_chat(channel_id)
                    link = f"https://t.me/{chat.username}" if chat.username else await chat.export_invite_link()
                    print(link, "Middleware Link")
                    btn.button(text=f"❌ {chat.title}", url=link)
                except:
                    continue

        if final_status:
            return await handler(event, data)
        else:
            btn.button(text="🔄 Tekshirish", callback_data=CheckSubCallback(check=False))
            btn.adjust(1)
            
            text = "🔔 *Davom etish uchun barcha kanallarga obuna bo‘ling!*"
            if event.message:
                await event.message.answer(text, reply_markup=btn.as_markup())
            elif event.callback_query:
                await event.callback_query.message.answer(text, reply_markup=btn.as_markup())
            return # Handlerga o'tmaydi

# class UserCheckMiddleware(BaseMiddleware):
#     async def __call__(
#         self,
#         handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
#         event: Update,
#         data: Dict[str, Any]
#     ) -> bool:
#         btn = InlineKeyboardBuilder()
#         user = event.from_user
#         final_status = True
#         CHANNELS = db.select_all_channels()
#         if CHANNELS:
#             for channel in CHANNELS:
#                 status = True
#                 try:
#                     status = await checksubscription(user_id=user.id, channel=channel[-1])
#                 except Exception as e:
#                     print(f"Subscription check error: {e}")

#                 final_status = final_status and status

#                 try:
#                     chat = await bot.get_chat(chat_id=channel[-1])
#                     if status:
#                         btn.button(text=f"✅ {chat.title}", url=f"{await chat.export_invite_link()}")
#                     else:
#                         btn.button(text=f"❌ {chat.title}", url=f"{await chat.export_invite_link()}")
#                 except Exception as e:
#                     print(e)
#                     pass

#             if final_status:
#                 await handler(event, data)
#             else:
#                 btn.button(
#                     text="🔄 Tekshirish",
#                     callback_data=CheckSubCallback(check=False)
#                 )
#                 btn.adjust(1)
#                 await event.answer(
#                     "🔔 *Davom etish uchun barcha kanallarga obuna bo‘ling!*\n\n"
#                     "❗️ Agar obuna bo‘lishda xatolik yuz bergan bo‘lsa, "
#                     "*/start* buyrug‘ini qayta bosib, yana urinib ko‘ring.",
#                     reply_markup=btn.as_markup()
#                 )
#         else:
#             await handler(event, data)



