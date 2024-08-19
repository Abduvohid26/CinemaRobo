from aiogram.filters.state import State, StatesGroup


class TextSend(StatesGroup):
    text = State()
    url = State()
    check = State()

class PhotoSend(StatesGroup):
    photo = State()
    url = State()
    check = State()


class VideoSend(StatesGroup):
    video = State()
    url = State()
    check = State()