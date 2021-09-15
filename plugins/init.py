from core import VK
import sys
from plugins.db import cursor as db, con


class main:
    triggers = ['init']

    def execute(self, vk : VK, peer : int, **mess):
        if "-init" in sys.argv:
            db.execute("CREATE TABLE IF NOT EXISTS moders   (vk_id INT NOT NULL PRIMARY KEY, event INT DEFAULT 0, days_without_posts INT DEFAULT 0, UNIQUE(vk_id))")
            db.execute("CREATE TABLE IF NOT EXISTS vacation (vk_id INT NOT NULL PRIMARY KEY, date_of_start TEXT NOT NULL, date_of_end TEXT NOT NULL, UNIQUE(vk_id))")
            db.execute("CREATE TABLE IF NOT EXISTS admins   (vk_id INT NOT NULL, UNIQUE(vk_id))")
            db.execute("CREATE TABLE IF NOT EXISTS counter  (vk_id INT NOT NULL, posts INT DEFAULT 0, UNIQUE(vk_id))")
            con.commit()
            vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message="+")

        