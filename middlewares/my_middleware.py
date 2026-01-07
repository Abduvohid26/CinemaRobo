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
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        # Faqat Message yoki CallbackQuery bo'lsa tekshiramiz
        message = event.message or event.callback_query.message
        user = event.message.from_user if event.message else event.callback_query.from_user
        
        if not user:
            return await handler(event, data)

        # 1. Barcha kanallarni birlashtirish (Static + DB)
        all_channels = list(CHANNELS_STATIC)
        db_channels = db.select_all_channels()
        if db_channels:
            for ch in db_channels:
                ch_id = ch[-1]
                if ch_id not in all_channels:
                    all_channels.append(ch_id)

        btn = InlineKeyboardBuilder()
        final_status = True

        # 2. Kanallarni tekshirish
        for channel_id in all_channels:
            try:
                # Obunani tekshirish
                status = await checksubscription(user_id=user.id, channel=channel_id)
                final_status = final_status and status

                # Kanal ma'lumotlarini olish
                chat = await bot.get_chat(chat_id=channel_id)
                
                # Havola yaratish (Invite link muammosini oldini olish)
                if chat.username:
                    invite_link = f"https://t.me/{chat.username}"
                else:
                    # Private kanal bo'lsa, avvalgi linkni olamiz yoki yangi export qilamiz
                    invite_link = chat.invite_link or await chat.export_invite_link()

                btn.button(
                    text=f"{'✅' if status else '❌'} {chat.title}",
                    url=invite_link
                )
            except Exception as e:
                print(f"Middleware xatolik ({channel_id}): {e}")
                continue

        # 3. Agar hamma kanalga a'zo bo'lsa, davom ettiramiz
        if final_status:
            return await handler(event, data)
        
        # 4. Agar a'zo bo'lmasa, xabar yuboramiz
        btn.button(
            text="🔄 Tekshirish",
            callback_data=CheckSubCallback(check=False)
        )
        btn.adjust(1)

        text = (
            "🔔 <b>Davom etish uchun barcha kanallarga obuna bo‘ling!</b>\n\n"
            "❗️ Obuna bo‘lgach 'Tekshirish' tugmasini bosing."
        )

        # Agar bu callback_query bo'lsa (Tekshirish tugmasi bosilgan bo'lsa)
        if event.callback_query:
            await event.callback_query.answer("⚠️ Hali hamma kanallarga a'zo emassiz!", show_alert=True)
            # Eski xabarni yangilaymiz
            try:
                await event.callback_query.message.edit_text(text=text, reply_markup=btn.as_markup(), parse_mode="HTML")
            except:
                pass
        else:
            # Yangi xabar yuboramiz
            await message.answer(text=text, reply_markup=btn.as_markup(), parse_mode="HTML")
            
        return  # Handlerga o'tib ketishni to'xtatamiz