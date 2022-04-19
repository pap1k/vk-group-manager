from core import VK
from plugins.db import cursor as db
from plugins.db import con

class main:
    triggers = [['flushestat', 'Сбрасывает стату ВСЕХ ивентов']]

    def execute(self, vk : VK, peer, **mess):
        userinfo = db.execute("SELECT * FROM admins WHERE vk_id = ?", (mess['from_id'],))
        if len(userinfo.fetchall()) == 1:
            db.execute("DELETE FROM reports")
            con.commit()
            vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message="[BOT]\nВсе отчеты удалены")
        else:
            vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message="[BOT]\nВы не можете использовать эту команду")