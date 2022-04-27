from core import VK
import json, os
from datetime import date
from plugins.db import cursor as db
from plugins.db import con

class main:
    triggers = [['getlog', 'Скидывает log.txt']]

    def execute(self, vk : VK, reply, **mess):
        ainfo = db.execute("SELECT * FROM admins WHERE vk_id = ?", (mess['from_id'],)).fetchall()
        if len(ainfo) > 0:
            txt = open("log.txt", "r", encoding="utf-8").read()
            reply(txt)
        else: reply("Вы не можете использовать эту команду")