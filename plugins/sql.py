from core import VK
from plugins.db import cursor as db, con
from perms import Perms

class main:
    triggers = [['sql', 'Выполняет SQL запрос в БД']]
    perm = Perms.Dev
    def execute(self, reply, **mess):
        r = db.execute(' '.join(mess['text'].split(' ')[1:]))
        con.commit()
        r.fetchall()
        print(r)
        reply("Done")