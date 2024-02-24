from core import VK
import sys
from plugins.db import cursor as db, con
from perms import Perms

class main:
    triggers = [['addadmin', 'Привелегирует пользователя админ правами в боте'], ['deleteadmin', 'Отбирает права адина у пользователя в боте']]
    target = True
    perm = Perms.Dev
    def execute(self, vk : VK, reply, **mess):
        db.execute("CREATE TABLE IF NOT EXISTS admins (vk_id INT NOT NULL)")

        data = db.execute("SELECT * FROM admins WHERE vk_id = ?", (mess['userId'],))

        if mess['cmd'] == "addadmin":
            if len(data.fetchall()) == 0:
                db.execute("INSERT INTO admins(vk_id) VALUES(?)", (mess['userId'],))

                name = vk.api("users.get", user_ids=mess['userId'])[0]

                m = f"{name['first_name']} {name['last_name']} назначен админом в боте"
                reply(m)
            else:
                reply("Указанный пользователь уже админ")
        else:
            if len(data.fetchall()) > 0:
                db.execute("DELETE FROM admins WHERE vk_id = ?", (mess['userId'],))

                name = vk.api("users.get", user_ids=mess['userId'])[0]

                m = f"{name['first_name']} {name['last_name']} снят с поста админа в боте"
                reply(m)
            else:
                reply("Указанный пользователь не админ")

        con.commit()
            
