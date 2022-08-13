from core import VK
from plugins.db import cursor as db
from perms import Perms

def getreb(table, uid):
    for user in table:
        if str(user[0]) == str(uid):
            return user[4]
    return -1

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

        ids = ','.join(events) +','+','.join(moders) #make string like '123,3213,4214235,5243235,3214235,412'
        names = vk.api("users.get", user_ids=ids)
        i = 0
        events_names = ""
        moders_names = ""
        for user in names:
            rebs = getreb(table, user['id'])
            if i < len(events):
                events_names += "[id"+str(user['id'])+"|"+user['first_name'] + " " + user['last_name']+"] [ВЫГОВОРЫ: " + ("(ошибка)" if rebs == -1 else str(rebs)) +"]"
                if user['id'] in [id[0] for id in vac]:
                    events_names += " [отпуск]"
                events_names += '\n'
            else:
                moders_names += "[id"+str(user['id'])+"|"+user['first_name'] + " " + user['last_name']+"] [ВЫГОВОРЫ: " + ("(ошибка)" if rebs == -1 else str(rebs)) +"]"
                if user['id'] in [id[0] for id in vac]:
                    moders_names += " [отпуск]"
                moders_names += '\n'
            i+=1
        message = "Обычные модеры:\n"+moders_names+"---------------\nEvent-модеры:\n"+events_names
        reply(message)