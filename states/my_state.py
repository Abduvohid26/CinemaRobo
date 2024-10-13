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


class VideoChannelSend(StatesGroup):
    start = State()
    caption = State()


class VideoChannelSerialSend(StatesGroup):
    start = State()
    caption = State()


class VideoChannelSerialSendExist(StatesGroup):
    post_id = State()
    start = State()
    caption = State()

