from core import VK
from plugins.db import cursor as db, con
from perms import Perms
import config, sys
import plugins.count


class main:
    triggers = ['test']
    perm = Perms.Admin
    target = True
    def execute(self, vk : VK, peer, userId, reply, **mess):
        if '-dev' in sys.argv:
            db.execute("UPDATE rebs SET isactive = 0 WHERE id = (SELECT id FROM rebs WHERE isactive = 1 AND vk_id = ? LIMIT 1 ORDER BY id)", (userId,))
            reply("Работает")
        else:
            vk.api("messages.send", peer_id=peer, message="Программа не в -dev режиме", reply_to=mess['id'])