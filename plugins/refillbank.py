import datetime
from plugins.db import cursor as db
from plugins.db import con
import re
from perms import Perms

def date(unixtime, format = '%d.%m.%Y %H:%M:%S'):
    d = datetime.datetime.fromtimestamp(unixtime)
    return d.strftime(format)

class main:
    triggers = [['refillbank', 'Устанавливает всем модерам'], ['rebank', "Аналог"]]
    perm = Perms.Admin

    def execute(self, reply, cmd, userId, **mess):
        #GET MONEY
        mess['text'] = re.sub(r'[ ]+', ' ', mess['text'])
        if len(mess['text'].split(' ')) < 2:
            return reply("Укажите сумму (число)")
        s = int(mess['text'].split(' ')[1].strip())
        if not s and s != 0:
            return reply("Укажите сумму (число)")
        db.execute("UPDATE moders SET money_left = ?", (s,))
        reply(f"Вы установили остаток средств = {s} для всех ивент модеров")
        con.commit()