from core import VK
from plugins.db import cursor as db, con
import datetime, time

def date(unixtime, format = '%d.%m.%Y %H:%M:%S'):
    d = datetime.datetime.fromtimestamp(unixtime)
    return d.strftime(format)

def getDayCase(num):
    if str(num)[-1] == "1": return "день"
    elif int(str(num)[:1]) in range(5,10) or str(num)[-1] == "0": return "дней"
    else: return "дня"

class main:
    triggers = [['vac', 'Кидает модера в отпуск на указанный срок в днях'], ['unvac', 'Выводит модера из отпуска']]
    target = True

    def execute(self, vk : VK, peer, **mess):
        userinfo = db.execute("SELECT * FROM admins WHERE vk_id = ?", (mess['from_id'],))

        if len(userinfo.fetchall()) == 1:

            data = db.execute("SELECT * FROM vacation WHERE vk_id = ?", (mess['userId'],)).fetchall()
                
            name = vk.api("users.get", user_ids=mess['userId'])[0]

            if mess['cmd'] == 'vac':
                if len(mess['text'].split(' ')) < 3:
                    return vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message="[BOT]\Ошибка. Укажите количество дней")
                days = int(mess['text'].split(' ')[2].strip())
                if not days:
                    return vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message="[BOT]\Ошибка. Количество дней это число")
                if days <= 0 or days > 14:
                    return vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message="[BOT]\Ошибка. Количество дней должно быть в диапазоне 1:14")

                if len(data) == 0:
                    dates = [date(time.time(), "%d.%m.%Y"), date(time.time()+days*24*60*60, "%d.%m.%Y")]
                    db.execute("INSERT INTO vacation(vk_id, date_of_start, date_of_end) VALUES(?, ?, ?)", (mess['userId'], dates[0], dates[1]))
                    m = f"{name['first_name']} {name['last_name']} был отправлен в отпуск до {dates[1]} (на {days} {getDayCase(days)})"

                    vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message=m)

                else:
                    vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message=f"[BOT]\nУказанный пользователь уже находится в отпуске. Выдан {data[0][1]} до {data[0][2]}")
            else:
                if len(data) == 0:
                    vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message="[BOT]\nУказанный пользователь не находится в отпуске")
                else:
                    db.execute("DELETE FROM vacation WHERE vk_id = ?", (mess['userId'],))
                    vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message=f"[BOT]\nМодер {name['first_name']} {name['last_name']} убран из отпуска.")
            con.commit()
        else:
            vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message="[BOT]\nВы не можете использовать эту команду")