from aiogram.utils.keyboard import InlineKeyboardBuilder


def buttons(film_id):
    btn = InlineKeyboardBuilder()
    btn.button(text='♻️ Dostlarga ulashish', switch_inline_query=film_id)
    btn.button(text='❌ O\'chirish', callback_data='delete')
    btn.adjust(1)
    return btn.as_markup()
