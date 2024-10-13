from environs import Env
env = Env()
env.read_env()
BOT_TOKEN=env.str('BOT_TOKEN')
ADMINS=env.list('ADMINS')
CHANNELS = [-1002008368827, ]
KINO_CHANNEL = [-1002035781732]