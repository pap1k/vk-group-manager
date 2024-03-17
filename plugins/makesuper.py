from core import VK
from plugins.db import cursor as db
from plugins.db import con
from perms import Perms
import time, datetime

class main:
    triggers = [['makesuper', 'Выдает модератору статус суупр модера'], ['dismisssuper', 'Снимает стутас супер пользователя']]
    target = True
    perm = Perms.Admin
    def execute(self, userId, cmd, reply, **message):
        moderinfo = db.execute("SELECT super FROM moders WHERE vk_id = ?", (userId,)).fetchall()
        if len(moderinfo) > 0:
            if cmd == 'makesuper':
                db.execute("UPDATE moders SET super = 1 WHERE vk_id = ?", (userId,))
                reply(f"Вы назначили [id{userId}|модератора] супер-модератором")
            else:
                db.execute("UPDATE moders SET super = 0 WHERE vk_id = ?", (userId,))
                reply(f"Вы сняли с [id{userId}|модератора] статус супер-модератора")
            con.commit()
        else:
            reply("Указанный пользователь не является модератором")