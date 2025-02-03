a="[Behzod + https://validators.readthedocs.io/en/latest/]Akbar-https://validators.readthedocs.io/en/latest[Akbar+https://validators.readthedocs.io/en/latest]"
import validators
def check_urls(text):
        havola = ''
        for i in text.split('['):
            for j in i.split(']'):
                if j:

                    if j.rfind('+')!=-1:
                        link  = j[j.rfind('+')+1:]
                        try:
                           validators.url(link)

                           havola+=j+"\n"
                        except Exception as e:
                           print(e)
                    else:
                        pass
                else:
                    pass
        return havola
import os
from loader import bot

async def get_data(chat_id):
    print('salom')
    db_path = 'data/main.db'
    if os.path.exists(db_path):
        with open(db_path, 'rb') as doc:
            await bot.send_document(chat_id, document=doc, caption='Main db file')
    else:
        await bot.send_message(chat_id, text="Main db file topilmadi")