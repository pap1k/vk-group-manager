from core import VK
from plugins.db import cursor as db, con
import config, sys


class main:
    triggers = ['test']
    
    def execute(self, vk : VK, peer, **mess):
        if '-dev' in sys.argv:
            posts = db.execute("SELECT * FROM counter").fetchall()
            print(posts)
        else:
            vk.api("messages.send", peer_id=peer, message="Программа не в -dev режиме", reply_to=mess['id'])