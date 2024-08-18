from environs import Env
env = Env()
env.read_env()
BOT_TOKEN=env.str('BOT_TOKEN')
ADMINS=env.list('ADMINS')
CHANNELS = ['-1002247871547', '-1002171770041']
