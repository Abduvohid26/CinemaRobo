# from environs import Env
# env = Env()
# env.read_env()
from decouple import config
# BOT_TOKEN=env.str('BOT_TOKEN')
BOT_TOKEN=config('BOT_TOKEN')
# ADMINS=env.list('ADMINS')
ADMINS = [816660001, 5700964012]
KINO_CHANNEL = [-1002035781732]