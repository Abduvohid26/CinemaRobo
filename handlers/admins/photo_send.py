from aiogram import types, F, html
from loader import bot, dp, db
from states.my_state import PhotoSend
from filters.admin_bot import IsBotAdmin
from aiogram.fsm.context import FSMContext
from keyboards.default.buttons import get_before_url, send_button, admin_button, rek_types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from check_url import check_urls
@dp.message(F.text == '📷 Rasm', IsBotAdmin())
async def text_send(message: types.Message, state: FSMContext):
    await message.answer(html.bold('Post rasmini yuboring'), reply_markup=get_before_url())
    await state.set_state(PhotoSend.photo)

@dp.message(PhotoSend.photo, IsBotAdmin())
async def get_message_text(message: types.Message, state: FSMContext):
    if message.content_type == 'photo':
        await state.update_data(
            {
                'photo': message.photo[-1].file_id,
                'caption': message.caption
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
        await state.set_state(PhotoSend.url)
    else:
        await message.answer(html.bold('Post Rasmini yuboring'), reply_markup=get_before_url())
        await state.set_state(PhotoSend.photo)

@dp.message(F.text == '🔙 Orqaga', IsBotAdmin(), PhotoSend.photo)
async def render_admin_panel(message: types.Message, state: FSMContext):
    await message.answer('Admin Panel', reply_markup=admin_button())
    await state.clear()

@dp.message(F.text == '📌 Bekor qilish', IsBotAdmin(), PhotoSend.url)
async def render_rek_type_panel(message: types.Message, state: FSMContext):
    await message.answer('📲  Reklama yubiorish turini tanlang:', reply_markup=rek_types())
    await state.clear()

@dp.message(F.text == '📌 Bekor qilish', IsBotAdmin(), PhotoSend.check)
async def render_rek_type_panel(message: types.Message, state: FSMContext):
    await message.answer('📲  Reklama yubiorish turini tanlang:', reply_markup=rek_types())
    await state.clear()

@dp.message(PhotoSend.url, IsBotAdmin())
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
        await message.answer_photo(photo=data['photo'], reply_markup=btn.as_markup(), caption=data['caption'])
        await message.answer(f"Agar tayyor bolsa '📤 Yuborish' tugmasini bosing!' tugmasini bosing", reply_markup=send_button())
        await state.set_state(PhotoSend.check)
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
        await state.set_state(PhotoSend.url)


@dp.message(F.text == '📤 Yuborish', IsBotAdmin(), PhotoSend.check)
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
                await bot.send_photo(chat_id=i[-2], photo=data['photo'], reply_markup=btn.as_markup(row_width=1), caption=data['caption'])
                counter += 1
            except Exception as e:
                print(e)
        await message.answer(f'{counter} kishiga xabar yuborildi', reply_markup=admin_button())
    else:
        counter = 0
        for i in users:
            try:
                await bot.send_photo(photo=data['photo'], chat_id=i[-2])
                counter += 1
            except Exception as e:
                print(e)
        await message.answer(f"{counter} kishiga xabar yuborildi!", reply_markup=admin_button())
    await state.clear()