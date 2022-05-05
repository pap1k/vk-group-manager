import datetime, time
from core import VK
from plugins.db import cursor as db
from plugins.db import con

def date(unixtime, format = '%d.%m.%Y %H:%M:%S'):
    d = datetime.datetime.fromtimestamp(unixtime)
    return d.strftime(format)

class main:
    triggers = [['cmdlist', 'Показывает список всех команд и их описание']]

    def execute(self, vk : VK, peer, plist, **mess):
        userinfo = db.execute("SELECT * FROM admins WHERE vk_id = ?", (mess['from_id'],))
        if len(userinfo.fetchall()) == 1:
            txt = ""
            for plugin in plist:
                for trigger in plugin.main.triggers:
                    if type(trigger) == list:
                        txt += f"[id0|/{trigger[0]}] : {trigger[1]}"
                    else:
                        txt += f"[id0|/{trigger}]"
                    txt += "\n"
            vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message="[BOT]\n"+txt)
        else:
            vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message="[BOT]\nу кого то хуй в говне")
        