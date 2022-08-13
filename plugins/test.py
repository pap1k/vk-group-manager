from core import VK
from plugins.db import cursor as db, con
from perms import Perms
import config, sys
import plugins.count


class main:
    triggers = ['test']
    perm = Perms.Admin
    def execute(self, vk : VK, peer, reply, **mess):
        if '-dev' in sys.argv:
            reply("Работает")
        else:
            vk.api("messages.send", peer_id=peer, message="Программа не в -dev режиме", reply_to=mess['id'])