import datetime, time
from core import VK
from plugins.db import cursor as db
from plugins.db import con

def date(unixtime, format = '%d.%m.%Y %H:%M:%S'):
    d = datetime.datetime.fromtimestamp(unixtime)
    return d.strftime(format)

class main:
    triggers = ['estat', 'eventstat']
    target = True

    def execute(self, vk : VK, peer, userId, **mess):
        userinfo = db.execute("SELECT * FROM admins WHERE vk_id = ?", (mess['from_id'],))
        if len(userinfo.fetchall()) == 1:
            eventinfo = db.execute("SELECT * FROM reports WHERE vk_id = ?", (userId,)).fetchall()
            if len(eventinfo) > 0:
                reporttext = "Список отчетов модера:\n"
                spent = 0
                for row in eventinfo:
                    reporttext += f"[{row[0]}]{row[4]} -- {row[2]} -> {row[3]}\n"
                    spent += row[2]#prize
                reporttext += f"\nВсего потрачено: {spent}\nВсего отчетов: {len(eventinfo)}"
                vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message="[BOT]\n"+reporttext)
            else:
                vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message="[BOT]\nПо данным бота, указанный модер не сдал ни одного отчета")
        else:
            vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message="[BOT]\nВы не можете использовать эту команду")