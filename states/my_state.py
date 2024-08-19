from aiogram.filters.state import State, StatesGroup


class TextSend(StatesGroup):
    text = State()
    url = State()
    check = State()
