from xmlrpc.client import boolean

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
class ChooseCallBackData(CallbackData, prefix='ikb26'):
    boolean: bool

def buttons(film_id):
    btn = InlineKeyboardBuilder()
    btn.button(text='♻️ Dostlarga ulashish', switch_inline_query=film_id)
    btn.button(text='❌ O\'chirish', callback_data='delete')
    btn.adjust(1)
    return btn.as_markup()


def choose_button():
    btn = InlineKeyboardBuilder()
    btn.button(text="♻️ Mavjud Serialga qo'shish", callback_data=ChooseCallBackData(boolean=True))
    btn.button(text="🆕 Yangi Serial qo'shish", callback_data=ChooseCallBackData(boolean=False))
    btn.adjust(2)
    return btn.as_markup()


def back():
    btn = InlineKeyboardBuilder()
    btn.button(text="⬅️ Orqaga")
    btn.adjust(1)
    return btn.as_markup()
