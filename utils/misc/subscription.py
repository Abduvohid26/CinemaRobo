# from loader import bot
# from aiogram import types
# from typing import Union, List
#
#
# async def checksubscription(user_id, channel: Union[int, str, List[Union[int, str]]]) -> bool:
#     if isinstance(channel, list):
#         for i in channel:
#             member = await bot.get_chat_member(chat_id=i, user_id=user_id)
#             status = member.status
#             if status not in ['creator', 'administrator', 'member']:
#                 return False
#         return True
#     else:
#         member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
#         status = member.status
#         return status in ['creator', 'administrator', 'member']
#
#
from loader import bot
from aiogram import types
from typing import Union
async def checksubscription(user_id,channel:Union[int,str]) -> bool:
    member = await bot.get_chat_member(chat_id=channel,user_id=user_id)
    status = member.status
    if status=='creator' or status=='administrator' or status=='member':
        return True
    else:
        return False

