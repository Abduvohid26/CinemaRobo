from aiogram import BaseMiddleware
from aiogram.types import Message,Update, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import *
from loader import bot, db
# from data.config import CHANNELS
from utils.misc.subscription import checksubscription
from aiogram.filters.callback_data import CallbackData
import logging
logger = logging.getLogger(__name__)

class CheckSubCallback(CallbackData,prefix='check'):
    check :bool

CHANNELS_STATIC = ['@abduvohiddev', '@Xabarnomada', '@Lidernoma', '@Biznes_savodxonlik']


class UserCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any]
    ) -> Any:

        # Faqat Message va CallbackQuery uchun
        if not isinstance(event, (Message, CallbackQuery)):
            return await handler(event, data)

        # user ni to‘g‘ri olish
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
            status = await checksubscription(
                user_id=user.id,
                channel=channel_id
            )
            final_status &= status

            if not status:
                try:
                    chat = await bot.get_chat(channel_id)
                    link = (
                        f"https://t.me/{chat.username}"
                        if chat.username
                        else await chat.export_invite_link()
                    )
                    logger.info("%s: Link Middleware", link)
                    btn.button(text=f"❌ {chat.title}", url=link)
                except Exception as e:
                    logger.error("Channel error: %s", e)
                    continue

        if final_status:
            return await handler(event, data)

        # ❌ Obuna bo‘lmaganlar uchun
        btn.button(
            text="🔄 Tekshirish",
            callback_data=CheckSubCallback(check=False)
        )
        btn.adjust(1)

        text = "🔔 *Davom etish uchun barcha kanallarga obuna bo‘ling!*"

        if isinstance(event, Message):
            await event.answer(text, reply_markup=btn.as_markup())
        elif isinstance(event, CallbackQuery):
            await event.message.answer(text, reply_markup=btn.as_markup())

        return

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



