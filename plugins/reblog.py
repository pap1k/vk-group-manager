from core import VK
from plugins.db import cursor as db
from plugins.db import con
from perms import Perms
import re

def getUserIdFromMentor(txt):
    found_id = re.findall(r"\[id(\d+)\|.+\]", txt)
    if len(found_id) == 1:
        return int(found_id[0])
    return False

class main:
    triggers = [['reblog', 'Показывает лог выговоров. Если упомнянуть модера, показывает только его выговоры']]

    perm = Perms.Admin
    def execute(self, userId, cmd, reply, **_):
        moderinfo = db.execute("SELECT rebs FROM moders WHERE vk_id = ?", (userId,)).fetchall()
        print(moderinfo)
        if len(moderinfo) > 0:
            act = 1 if cmd == 'reb' else -1
            newrebs = int(moderinfo[0][0]) + 1*act
            print(newrebs)
            if newrebs < 0:
                reply("Количество выговоров не может быть меньше 0")
                return
            
            db.execute("UPDATE moders SET rebs = ? WHERE vk_id = ?", (newrebs,userId))
            con.commit()
            action = "выдали" if act == 1 else "сняли"
            reply(f"Вы {action} выговор модератору. Статистика доступна в /list")
        else:
            reply("Указанный пользователь не является модератором")