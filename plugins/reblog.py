from plugins.db import cursor as db
from plugins.db import con
from perms import Perms
import re

def getUserIdFromMentor(txt):
    found_id = re.findall(r"\[id(\d+)\|.+\]", txt)
    if len(found_id) == 1:
        return int(found_id[0])
    return False

def buildLog(info):
    mess = ""
    for reb in info:
        addinfo = ""
        dbinfo = db.execute("SELECT * FROM moders WHERE event = 1 AND vk_id = ?", (reb[1],)).fetchall()
        if len(dbinfo) > 0:
            addinfo = " [E]"
        if reb[5]:
            addinfo += " C: "+reb[5]
        if reb[2] == 1: #выдача
            mess = f"{reb[4]} [id{reb[3]}|Админ] ВЫДАЛ выговор [id{reb[1]}|модератору]{addinfo}\n" + mess
        elif reb[2] == 0: #снятие
            mess = f"{reb[4]} [id{reb[3]}|Админ] СНЯЛ выговор [id{reb[1]}|модератору]{addinfo}\n" + mess
        else:
            mess = f"Невозможно определить тип действия ({reb[2]}), id = {reb[0]}\n"  + mess
    return mess

class main:
    triggers = [['reblog', 'Показывает лог выговоров. Если упомнянуть модера, показывает только его выговоры']]
    perm = Perms.Admin
    def execute(self, userId, cmd, reply, **_):
        if userId:
            moderinfo = db.execute("SELECT rebs FROM moders WHERE vk_id = ?", (userId,)).fetchall()
            if len(moderinfo) > 0:
                info = db.execute("SELECT * FROM rebs WHERE vk_id = ? ORDER BY id desc LIMIT 30 ", (userId,)).fetchall()
            else:
                return reply("Указанный пользователь не является модератором")
        else:
            info = db.execute("SELECT * FROM rebs ORDER BY id desc LIMIT 30 ").fetchall()

        mess = "Лог действий c выговорами\n\n"
        mess += buildLog(info)
        reply(mess)
        