from core import VK
from plugins.db import cursor as db, con
import config, sys


class main:
    triggers = ['mounth', 'monstat']

    def execute(self, vk : VK, peer, **mess):
        userinfo = db.execute("SELECT * FROM admins WHERE vk_id = ?", (mess['from_id'],))
        if len(userinfo.fetchall()) == 1:
            data = db.execute("SELECT * FROM counter").fetchall()
            ids = [str(i[0]) for i in data]
            names = vk.api("users.get", user_ids=",".join(ids))

            res = "Отчет по постам на текущий момент:\n"
            for i in range(len(data)):
                res += f"{names[i]['first_name']} {names[i]['last_name']} - {data[i][1]}\n"

            vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message=res)

        else:
            vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message="[BOT]\nВы не можете использовать эту команду")