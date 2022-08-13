from core import VK
from plugins.db import cursor as db
from plugins.db import con
from perms import Perms

class main:
    triggers = [['reb', 'Выдает выговор модеру'], ['unreb', 'Снимает выговор модеру']]
    target = True
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