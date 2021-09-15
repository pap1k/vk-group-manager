from core import VK
from plugins.db import cursor as db, con


class main:
    triggers = ['sql']
    def execute(self, vk : VK, peer : int, **mess):
        if mess['from_id'] == 218999719:
            r = db.execute(' '.join(mess['text'].split(' ')[1:]))
            con.commit()
            r.fetchall()
            print(r)
            vk.api("messages.send", peer_id=peer, message="Done", reply_to=mess['id'])
        else:
            vk.api("messages.send", peer_id=peer, message="JIagHo (нет)", reply_to=mess['id'])