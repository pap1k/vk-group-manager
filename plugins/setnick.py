from core import VK
from plugins.db import cursor as db, con
from perms import Perms

class main:
    triggers = [['mynick', 'Без параметров показывает ваш ник, находящийся в базе. При использовании /mynick [ник] обновляет ник в базе']]
    perm = Perms.Moder
    def execute(self, vk : VK, reply, **message):
        args = message['text'].split(' ')
        if len(args) == 2:
            db.execute("UPDATE moders SET nick = ? WHERE vk_id = ?", (args[1], message['from_id']))
            con.commit()
        res = "Ваш текущий ник "
        nick = db.execute("SELECT nick FROM moders WHERE vk_id = ?", (message['from_id'], )).fetchall()
        if nick == [] or type(nick[0]) != tuple or nick[0][0] == None:
            nick = "Не установлен"
        else:
            nick = nick[0][0]
        reply(res + nick)