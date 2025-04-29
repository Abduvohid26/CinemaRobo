from aiogram.utils.keyboard import ReplyKeyboardBuilder

def admin_button():
    btn = ReplyKeyboardBuilder()
    btn.button(text='📲 Reklama Yuborish')
    btn.button(text='👤 Obunachilar soni')
    btn.button(text="🎦 Kino qo'shish")
    btn.button(text="🎦 Serial qo'shish")
    btn.button(text='➕  Kanal qo\'shish')
    btn.button(text='♾️ Kanallar')
    btn.button(text='✖️ Kanal o\'chirish')
    btn.adjust(2)
    return btn.as_markup(resize_keyboard=True, one_time_keyboard=True, input_placeholder='Keraklli bolimni tanlang')


def rek_types():
    btn = ReplyKeyboardBuilder()
    btn.button(text='📝 Text')
    btn.button(text='📷 Rasm')
    btn.button(text='📹 Video')
    btn.button(text='🔙 Orqaga')
    btn.adjust(2)
    return btn.as_markup(resize_keyboard=True)

def get_before_url():
    btn = ReplyKeyboardBuilder()
    btn.button(text='📌 Bekor qilish')
    btn.adjust(1)
    return btn.as_markup(resize_keyboard=True, one_time_keyboard=True)

def send_button():
    btn = ReplyKeyboardBuilder()
    btn.button(text='📤 Yuborish')
    btn.button(text='📌 Bekor qilish')
    btn.adjust(2)
    return btn.as_markup(resize_keyboard=True)


from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class DeleteChannelCallback(CallbackData, prefix='ikb'):
    check:bool

def delete_channel_verify():
    btn = InlineKeyboardBuilder()
    btn.button(text="✅ Ha", callback_data=DeleteChannelCallback(check=True))
    btn.button(text="❌ Yo'q", callback_data=DeleteChannelCallback(check=False))
    btn.adjust(2)
    return btn.as_markup()