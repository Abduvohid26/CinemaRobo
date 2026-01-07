from aiogram import BaseMiddleware
from aiogram.types import Message,Update, CallbackQuery
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
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Any,  # Message yoki CallbackQuery bo'lishi mumkin
        data: Dict[str, Any]
    ) -> Any:
        
        # 1. User va Message obyektini aniqlab olamiz
        if isinstance(event, Message):
            user = event.from_user
            current_message = event
        elif isinstance(event, CallbackQuery):
            user = event.from_user
            current_message = event.message
            # "Tekshirish" tugmasi bosilganda cheksiz siklga tushmaslik uchun:
            if event.data.startswith("check"):
                return await handler(event, data)
        else:
            return await handler(event, data)

        if not user:
            return await handler(event, data)

        # 2. Kanallarni yig'amiz (Static + DB)
        all_channels = list(CHANNELS_STATIC)
        db_channels = db.select_all_channels()
        if db_channels:
            for ch in db_channels:
                ch_id = ch[-1]
                if ch_id not in all_channels:
                    all_channels.append(ch_id)

        btn = InlineKeyboardBuilder()
        final_status = True

        # 3. Obunani tekshirish
        for channel_id in all_channels:
            try:
                status = await checksubscription(user_id=user.id, channel=channel_id)
                final_status = final_status and status

                # Kanal ma'lumotlarini olish
                chat = await bot.get_chat(chat_id=channel_id)
                
                # Link yaratish (Invite link muammosini hal qilish)
                if chat.username:
                    invite_link = f"https://t.me/{chat.username}"
                else:
                    invite_link = chat.invite_link or await chat.export_invite_link()

                btn.button(
                    text=f"{'✅' if status else '❌'} {chat.title}",
                    url=invite_link
                )
            except Exception as e:
                print(f"Xatolik {channel_id} tekshirishda: {e}")
                continue

        # 4. Natijaga qarab javob berish
        if final_status:
            return await handler(event, data)
        else:
            btn.button(
                text="🔄 Tekshirish",
                callback_data=CheckSubCallback(check=False).pack()
            )
            btn.adjust(1)
            
            text = (
                "🔔 <b>Davom etish uchun barcha kanallarga obuna bo‘ling!</b>\n\n"
                "❗️ Obuna bo‘lgach 'Tekshirish' tugmasini bosing."
            )

            # Agar callback bo'lsa (tugma bosilgan bo'lsa) edit qilamiz
            if isinstance(event, CallbackQuery):
                await event.answer("⚠️ Hali hamma kanallarga a'zo emassiz!", show_alert=True)
                try:
                    await current_message.edit_text(text=text, reply_markup=btn.as_markup(), parse_mode="HTML")
                except:
                    pass
            else:
                # Yangi xabar yuboramiz
                await current_message.answer(text=text, reply_markup=btn.as_markup(), parse_mode="HTML")
            
            return # Handler ishga tushmaydi