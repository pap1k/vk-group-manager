from core import VK
from plugins.db import cursor as db
from plugins.db import con
from perms import Perms
import time, datetime

def date(unixtime, format = '%d.%m.%Y %H:%M:%S'):
    d = datetime.datetime.fromtimestamp(unixtime)
    return d.strftime(format)

class main:
    triggers = [['reb', 'Выдает выговор модеру'], ['unreb', 'Снимает выговор модеру']]
    target = True
    perm = Perms.Admin
    def execute(self, userId, cmd, reply, **message):
        moderinfo = db.execute("SELECT rebs FROM moders WHERE vk_id = ?", (userId,)).fetchall()
        if len(moderinfo) > 0:
            act = 1 if cmd == 'reb' else -1
            newrebs = int(moderinfo[0][0]) + 1*act
            if newrebs < 0:
                reply("Количество выговоров не может быть меньше 0")
                return
            if len(message['text'].split(' ')) > 2:
                db.execute("INSERT INTO rebs(vk_id, admin, action, date_of_reb, comment) VALUES(?,?,?,?,?)", (userId, message['from_id'], (act if act == 1 else 0), date(time.time()), ' '.join(message['text'].split(' ')[2:])))
            else:
                return reply("/reb [id] [причина]")
            db.execute("UPDATE moders SET rebs = ? WHERE vk_id = ?", (newrebs,userId))
            con.commit()
            action = "выдали" if act == 1 else "сняли"
            reply(f"Вы {action} выговор модератору. Статистика доступна в /list")
        else:
            reply("Указанный пользователь не является модератором")