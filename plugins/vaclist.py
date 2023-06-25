from plugins.db import cursor as db
import datetime
from perms import Perms

def date(unixtime, format = '%d.%m.%Y %H:%M:%S'):
    d = datetime.datetime.fromtimestamp(unixtime)
    return d.strftime(format)

class main:
    triggers = [['vaclist', 'Показывает список модеров в отпуске + их срок']]
    perm = Perms.Admin
    def execute(self, reply, **_):
        vaclist = db.execute("SELECT * FROM vacation").fetchall()
        if len(vaclist) > 0:
            mess = "Список модеров в отпуске:\n\n"
            for moder in vaclist:
                mess += f"[id{moder[0]}|Модератор] в отпуске С [{moder[1]}] ПО [{moder[2]}]\n"
            reply(mess)
        else:
            reply("Список модеров в отпуске пуст")
        