from core import VK
from plugins.db import cursor as db, con
import config, sys
import plugins.count


class main:
    triggers = ['test']
    
    def execute(self, vk : VK, peer, **mess):
        if '-dev' in sys.argv:
            counter = plugins.count.main()
            counter.execute(vk, peer, **mess)
        else:
            vk.api("messages.send", peer_id=peer, message="Программа не в -dev режиме", reply_to=mess['id'])