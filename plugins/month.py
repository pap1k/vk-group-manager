from core import VK
from plugins.db import cursor as db
from perms import Perms

class main:
    triggers = [['mounth', 'Формирует ответ по работе модеров с момента последенй чистки через /flush'], ['monstat', 'Аналог']]
    perm = Perms.Admin
    def execute(self, vk : VK, reply, **_):
        data = db.execute("SELECT * FROM counter").fetchall()
        ids = [str(i[0]) for i in data]
        names = vk.api("users.get", user_ids=",".join(ids))

        res = "Отчет по постам на текущий момент:\n"
        for i in range(len(data)):
            res += f"{names[i]['first_name']} {names[i]['last_name']} - {data[i][1]}\n"

        reply(res)