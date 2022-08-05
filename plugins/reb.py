import datetime
from core import VK
from plugins.db import cursor as db
from plugins.db import con

class main:
    triggers = [['reb', 'Выдает выговор модеру'], ['unreb', 'Снимает выговор модеру']]
    target = True

    def execute(self, vk : VK, peer, userId, cmd, reply, **mess):
        userinfo = db.execute("SELECT * FROM admins WHERE vk_id = ?", (mess['from_id'],))

        if len(userinfo.fetchall()) == 1:
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
        else:
            reply("Вы не можете использовать эту команду")