from aiogram import types, F, html
from loader import bot, dp, db
from states.my_state import TextSend
from filters.admin_bot import IsBotAdmin
from aiogram.fsm.context import FSMContext
from keyboards.default.buttons import get_before_url, send_button, admin_button, rek_types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from check_url import check_urls
@dp.message(F.text == '📝 Text', IsBotAdmin())
async def text_send(message: types.Message, state: FSMContext):
    await message.answer(html.bold('Post textini yuboring'), reply_markup=get_before_url())
    await state.set_state(TextSend.text)

@dp.message(TextSend.text, IsBotAdmin())
async def get_message_text(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        await state.update_data(
            {
                'text': message.text
            }
        )
        text = """
           Havolani quyidagi formatda yuborish:
            [tugma matn + havola]
            Misol: 
            [Tarjimon+https://t.me/abduvohid_coder]
            Bir qatorga bir nechta tugmalar qo'shish uchun yanagi qatorga yangi havolalar yozing.
            Format:
            [Birinchi matn + birinchi havola]
            [Ikkinchi matn + ikkinchi havola]
        """
        await message.answer(text=text, reply_markup=get_before_url())
        await state.set_state(TextSend.url)
    else:
        await message.answer(html.bold('Post textini yuboring'), reply_markup=get_before_url())
        await state.set_state(TextSend.text)

@dp.message(F.text == '🔙 Orqaga', IsBotAdmin(), TextSend.text)
async def render_admin_panel(message: types.Message, state: FSMContext):
    await message.answer('Admin Panel', reply_markup=admin_button())
    await state.clear()

@dp.message(F.text == '📌 Bekor qilish', IsBotAdmin(), TextSend.url)
async def render_rek_type_panel(message: types.Message, state: FSMContext):
    await message.answer('📲  Reklama yubiorish turini tanlang:', reply_markup=rek_types())
    await state.clear()

@dp.message(F.text == '📌 Bekor qilish', IsBotAdmin(), TextSend.check)
async def render_rek_type_panel(message: types.Message, state: FSMContext):
    await message.answer('📲  Reklama yubiorish turini tanlang:', reply_markup=rek_types())
    await state.clear()

@dp.message(TextSend.url, IsBotAdmin())
async def get_url(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        urls = check_urls(text=message.text)
        urls = urls if urls else None
        await state.update_data({
            'buttons': urls
        })
        data = await state.get_data()
        links = urls.splitlines()
        btn = InlineKeyboardBuilder()
        for link in links:
            manzil = link[link.rfind('+') + 1:]
            manzil = manzil.strip()
            text = link[:link.rfind('+')]
            text = text.strip()
            btn.button(text=text, url=manzil)
        btn.adjust(1)
        await message.answer(text=data['text'], reply_markup=btn.as_markup())
        await message.answer(f"Agar tayyor bolsa '📤 Yuborish' tugmasini bosing!' tugmasini bosing", reply_markup=send_button())
        await state.set_state(TextSend.check)
    else:
        text = "Havolani quyidagi formatda yuborish:\n" \
               "[tugma matni+havola]\n" \
               "Misol:\n" \
               "[Tarjimon+https://t.me/Behzod_Asliddinov]\n" \
               "Bir qatorga bir nechta tugmalar qo'shish uchun yangi qatorga yangi havolalarni yozing.\n" \
               "Format:\n" \
               "[Birinchi matn+birinchi havola]\n" \
               "[Ikkinchi matn+ikkinchi havola]"

        await message.answer(text, reply_markup=get_before_url())
        await state.set_state(TextSend.url)


@dp.message(F.text == '📤 Yuborish', IsBotAdmin(), TextSend.check)
async def send_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    users = db.select_all_users()
    if data.get('buttons', None):
        links = data['buttons'].splitlines()
        btn = InlineKeyboardBuilder()
        for link in links:
            manzil = link[link.rfind('+') + 1:]
            manzil = manzil.strip()
            text = link[:link.rfind('+')]
            text = text.strip()
            btn.button(text=text, url=manzil)
        btn.adjust(1)
        counter = 0
        for i in users:
            try:
                await bot.send_message(chat_id=i[-2], text=data['text'], reply_markup=btn.as_markup(row_width=1))
                counter += 1
            except Exception as e:
                print(e)
        await message.answer(f'{counter} kishiga xabar yuborildi', reply_markup=admin_button())
    else:
        text = data['text']
        counter = 0
        for i in users:
            try:
                await bot.send_message(text=text, chat_id=i[-2])
                counter += 1
            except Exception as e:
                print(e)
        await message.answer(f"{counter} kishiga xabar yuborildi!", reply_markup=admin_button())
    await state.clear()