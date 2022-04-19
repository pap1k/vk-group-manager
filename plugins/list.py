from core import VK
from plugins.db import cursor as db


class main:
    triggers = [['list', 'Показывает список всех модеров, ивентов. Показывает кто в отпуске']]
    
    def execute(self, vk : VK, peer, **mess):
        userinfo = db.execute("SELECT * FROM admins WHERE vk_id = ?", (mess['from_id'],))
        if len(userinfo.fetchall()) == 1:
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
                if i < len(events):
                    events_names += "[id"+str(user['id'])+"|"+user['first_name'] + " " + user['last_name']+"]"
                    if user['id'] in [id[0] for id in vac]:
                        events_names += " [отпуск]"
                    events_names += '\n'
                else:
                    moders_names += "[id"+str(user['id'])+"|"+user['first_name'] + " " + user['last_name']+"]"
                    if user['id'] in [id[0] for id in vac]:
                        moders_names += " [отпуск]"
                    moders_names += '\n'
                i+=1
            message = "Обычные модеры:\n"+moders_names+"---------------\nEvent-модеры:\n"+events_names
            vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message="[BOT]\n"+message)
        else:
            vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message="[BOT]\nВы не можете использовать эту команду")