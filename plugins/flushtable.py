from core import VK
from datetime import date
from plugins.db import cursor as db
from plugins.db import con

class main:
    triggers = [['flush', '[ОПАСНО]Сбрасывает статистику работы модеров'], ['cleartable', '[ОПАСНО]Аналог']]
    confirm = True

    def execute(self, vk : VK, peer, reply, **mess):
        userinfo = db.execute("SELECT * FROM admins WHERE vk_id = ?", (mess['from_id'],))
        if len(userinfo.fetchall()) == 1:
            if 'has_confirmation' in mess:
                if mess['has_confirmation'] in ['да', 'yes']:
                    # data = db.execute("SELECT * FROM counter")
                    # savedata = {}
                    # for one in data:
                    #     savedata[one[0]] = one[1]
                    # filename = "count_"+date.today().strftime("%d-%m-%Y")+".json"
                    # if not os.path.exists("backups/"):
                    #     os.mkdir("backups/")
                    # open("backups/"+filename, "w").write(json.dumps(savedata))

                    # db.execute("UPDATE moders SET rebs = 0")
                    # db.execute("DELETE FROM counter")
                    # con.commit()

                    vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message="Таблица статистики и выговоры модераторов очещены")
                else:
                    reply("Сброс статистики отменен")
            else:
                reply("Вы действительно хотите сбросить статистику работы всех модераторов? [да/нет]")

        else:
            vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message="[BOT]\nВы не можете использовать эту команду")