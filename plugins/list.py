from core import VK
from plugins.db import cursor as db
from perms import Perms

def getreb(table, uid):
    for user in table:
        if str(user[0]) == str(uid):
            return user[4]
    return -1

def getnick(table, uid):
    for user in table:
        if str(user[0]) == str(uid):
            return user[5]
    return None

def getsuper(table, uid):
    for user in table:
        if str(user[0]) == str(uid):
            return user[6]
    return None

class main:
    triggers = [['list', 'Показывает список всех модеров, ивентов. Показывает кто в отпуске. Показывает выговоры']]
    perm = Perms.Admin

    def execute(self, vk : VK, reply, **_):
        table = db.execute("SELECT * FROM moders").fetchall()
        vac = db.execute("SELECT vk_id FROM vacation")
        moders = []
        events = []
        for moder in table:
            if moder[1] == 1:
                events.append(str(moder[0]))
            if moder[1] == 0:
                moders.append(str(moder[0]))

        ids = ','.join(events) +','+','.join(moders)
        names = vk.api("users.get", user_ids=ids)

        i = 0
        mlist = ""
        vaclist = [id[0] for id in vac]
        for user in names:
            rebs = getreb(table, user['id'])
            nick = getnick(table, user['id'])
            sup = getsuper(table, user['id'])
            if nick == None:
                nick = "Не указан ник"
            if str(sup) == '1':
                mlist += "[S]"
            if i < len(events):
                mlist += "[E] "
            mlist += "[id"+str(user['id'])+"|"+user['first_name'] + " " + user['last_name']+f"] ({nick}) [ВЫГОВОРЫ: " + ("(ошибка)" if rebs == -1 else str(rebs)) +"]"
            if user['id'] in vaclist:
                    mlist += "[отпуск]"
            mlist += "\n"
            i+=1
        
        message = "Список модераторов:\n"+mlist
        reply(message)