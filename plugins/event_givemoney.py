import datetime
from plugins.db import cursor as db
from plugins.db import con
import re
from perms import Perms

def date(unixtime, format = '%d.%m.%Y %H:%M:%S'):
    d = datetime.datetime.fromtimestamp(unixtime)
    return d.strftime(format)

class main:
    triggers = [['emoney', 'Показывает сколько осталось денег у указанного инвента'], ['setemoney', "Обновляет деньги модера в базе"]]
    target = True
    perm = Perms.Admin

    def execute(self, reply, cmd, userId, **mess):
        #GET MONEY
        eventinfo = db.execute("SELECT * FROM moders WHERE vk_id = ? AND event = 1", (userId,)).fetchall()
        if len(eventinfo) > 0:
            if cmd == self.triggers[0][0]:
                reporttext = "Остаток средств по данным бота: "+str(eventinfo[0][3])
                reply("[BOT]\n"+reporttext)
            
            else:
                mess['text'] = re.sub(r'[ ]+', ' ', mess['text'])
                if len(mess['text'].split(' ')) < 3:
                    return reply("[BOT]\nУкажите сумму (число)")
                s = int(mess['text'].split(' ')[2].strip())
                if not s and s != 0:
                    return reply("[BOT]\nУкажите сумму (число)")
                db.execute("UPDATE moders SET money_left = ? WHERE vk_id = ?", (s, userId))
                reply(f"[BOT]\nВы установили остаток средств = {s}")
                con.commit()
        else:
            reply("[BOT]\nУказанный пользователь не является ивент модером.")