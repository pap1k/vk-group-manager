from core import VK
from plugins.db import cursor as db
from perms import Perms

class main:
    triggers = [['alist', 'Показывает список всех админов']]
    perm = Perms.Admin
    def execute(self, vk : VK, reply, **_):
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

        reply(message)