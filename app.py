import handlers
import middlewares
from loader import dp, bot, db
from aiogram.types.bot_command_scope_all_private_chats import BotCommandScopeAllPrivateChats
import asyncio
from utils.notify_admins import start, shutdown
from utils.set_botcommands import commands
from middlewares.my_middleware import UserCheckMiddleware
# Info
import logging
import sys


async def main():
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_my_commands(commands=commands,scope=BotCommandScopeAllPrivateChats(type='all_private_chats'))
        dp.startup.register(start)
        dp.shutdown.register(shutdown)
        dp.message.middleware(UserCheckMiddleware())
        # Create Users Table
        try:
            db.create_table_users()
        except:
            pass
        #############################
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
