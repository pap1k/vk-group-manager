from core import VK
from datetime import date
from plugins.db import cursor as db
from plugins.db import con
from perms import Perms
import os, json

class main:
    triggers = [['flush', '[ОПАСНО]Сбрасывает статистику работы модеров'], ['cleartable', '[ОПАСНО]Аналог']]
    confirm = True
    perm = Perms.Admin

    def execute(self, vk : VK, peer, reply, **mess):
        if 'has_confirmation' in mess:
            if mess['has_confirmation'] in ['да', 'yes']:
                data = db.execute("SELECT * FROM counter")
                savedata = {}
                for one in data:
                    savedata[one[0]] = one[1]
                filename = "count_"+date.today().strftime("%d-%m-%Y")+".json"
                if not os.path.exists("backups/"):
                    os.mkdir("backups/")
                open("backups/"+filename, "w").write(json.dumps(savedata))

                db.execute("UPDATE moders SET rebs = 0")
                db.execute("DELETE FROM counter")
                con.commit()

                reply("Таблица статистики и выговоры модераторов очещены")
            else:
                reply("Сброс статистики работы модераторов отменен")
        else:
            reply("Вы действительно хотите сбросить статистику работы всех модераторов? [да/нет]")