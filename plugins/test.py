from core import VK
from plugins.db import cursor as db, con
import config, sys
import plugins.count


class main:
    triggers = ['test']
    
    def execute(self, vk : VK, peer, reply, **mess):
        if '-dev' in sys.argv:
            n = ""
            for i in range(0, 200):
                n += f"[{i}] asdsdgsdgskdf jsdnf kjsndfjkansdfjk saf "
            reply(n)
        else:
            vk.api("messages.send", peer_id=peer, message="Программа не в -dev режиме", reply_to=mess['id'])