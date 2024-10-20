from environs import Env
env = Env()
env.read_env()
BOT_TOKEN=env.str('BOT_TOKEN')
# ADMINS=env.list('ADMINS')
ADMINS = [816660001, 5700964012]
CHANNELS = [-1002008368827, ]
KINO_CHANNEL = [-1002035781732]