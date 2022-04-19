from core import VK
from plugins.db import cursor as db


class main:
    triggers = [['alist', 'Показывает список всех админов']]
    
    def execute(self, vk : VK, peer, **mess):
        userinfo = db.execute("SELECT * FROM admins WHERE vk_id = ?", (mess['from_id'],))
        if len(userinfo.fetchall()) == 1:
            table = db.execute("SELECT * FROM admins").fetchall()
            admins = []
            for admin in table:
                admins.append(str(admin[0]))


            ids = ','.join(admins)
            names = vk.api("users.get", user_ids=ids)
            admin_names = ""
            for user in names:
               admin_names += user['first_name'] + " " + user['last_name']+" ["+str(user['id'])+"]\n"

            message = "Список добавленных:\n"+admin_names

            vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message="[BOT]\n"+message)
        else:
            vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message="[BOT]\nВы не можете использовать эту команду")