import datetime, time
from core import VK
from plugins.db import cursor as db
from plugins.db import con
import re

def date(unixtime, format = '%d.%m.%Y %H:%M:%S'):
    d = datetime.datetime.fromtimestamp(unixtime)
    return d.strftime(format)

class main:
    triggers = [['emoney', 'Показывает сколько осталось денег у указанного инвента'], ['setemoney', "Обновляет деньги модера в базе"]]
    target = True

    def execute(self, vk : VK, peer, cmd, userId, **mess):
        userinfo = db.execute("SELECT * FROM admins WHERE vk_id = ?", (mess['from_id'],))
        if len(userinfo.fetchall()) == 1:
            #GET MONEY
            eventinfo = db.execute("SELECT * FROM moders WHERE vk_id = ? AND event = 1", (userId,)).fetchall()
            if len(eventinfo) > 0:
                if cmd == self.triggers[0][0]:
                    reporttext = "Остаток средств по данным бота: "+str(eventinfo[0][3])
                    vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message="[BOT]\n"+reporttext)
                
                else:
                    mess['text'] = re.sub(r'[ ]+', ' ', mess['text'])
                    if len(mess['text'].split(' ')) < 3:
                        return vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message="[BOT]\nУкажите сумму (число)")
                    s = int(mess['text'].split(' ')[2].strip())
                    if not s and s != 0:
                        return vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message="[BOT]\nУкажите сумму (число)")
                    db.execute("UPDATE moders SET money_left = ? WHERE vk_id = ?", (s, userId))
                    vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message=f"[BOT]\nВы установили остаток средств = {s}")
                    con.commit()
            else:
                vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message="[BOT]\nУказанный пользователь не является ивент модером.")
        else:
            vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message="[BOT]\nВы не можете использовать эту команду")