from core import VK
from plugins.db import cursor as db, con
from perms import Perms

class main:
    triggers = [['makeevent', 'Назначает модера ивентом. Приглашает в ивент чат.'], ['dismissevent', 'Снимает модера с поста ивента, удаляет из чата'], ['unevent', 'Аналог']]
    target = True
    perm = Perms.Admin
    def execute(self, vk : VK, reply, **mess):
        db.execute("CREATE TABLE IF NOT EXISTS moders(vk_id INT NOT NULL, event INT DEFAULT 0)")

        data = db.execute("SELECT * FROM moders WHERE vk_id = ? AND event = 1", (mess['userId'],)).fetchall()
        
        name = vk.api("users.get", user_ids=mess['userId'])[0]

        #Проверка является ли чел модером вообще
        if len(db.execute("SELECT * FROM moders WHERE vk_id = ?", (mess['userId'],)).fetchall()) == 0:
            return reply("Указанный пользователь не является модером")

        #Назначение ивент-модером
        if mess['cmd'] == "makeevent":
            if len(data) == 0:
                db.execute("UPDATE moders SET event = 1 WHERE vk_id = ?", (mess['userId'],))

                reply(f"{name['first_name']} {name['last_name']} назначен ивент-модером")
            else:
                reply("Указанный пользователь уже является ивент-модером")

        #Снятие с поста ивент-модера
        else:
            if len(data) > 0:
                db.execute("UPDATE moders SET event = 0 WHERE vk_id = ?", (mess['userId'],))

                reply(f"{name['first_name']} {name['last_name']} снят с поста ивент-модера в боте")
            else:
                reply("Указанный пользователь не является ивент-модером")

        con.commit()