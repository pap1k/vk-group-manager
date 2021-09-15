from core import VK
from plugins.db import cursor as db, con
import config, datetime, time

def date(unixtime, format = '%d.%m.%Y %H:%M:%S'):
    d = datetime.datetime.fromtimestamp(unixtime)
    return d.strftime(format)

def getDayCase(num):
    if str(num)[-1] == "1": return "день"
    elif int(str(num)[:1]) in range(5,10) or str(num)[-1] == "0": return "дней"
    else: return "дня"

def findModer(moders, id):
    for moder in moders:
        if moder[0] == id:
            return moder
    return None

class main:
    triggers = ['daycount']
    
    def count(self, vk : VK, peer, test = False):
        moders = db.execute("SELECT * FROM moders").fetchall()
        vac = [id[0] for id in db.execute("SELECT vk_id FROM vacation").fetchall()]
        moders_days = {}
        for moder in moders:#Заполняем кто сколько дней не постил. Инфа из базы
            moders_days[moder[0]] = moder[2]

        posts = vk.api("wall.get", count=50, owner_id=0-config.GROUP_ID)

        ts = int(time.time())-24*60*60

        nohash = 0
        hashs = {
            "#ccold" : 0,
            "#ccnews" : 0,
            "#ccreport" : 0,
            "#ccvoice" : 0,
            "#ccspeak" : 0,
            "#ccproject" : 0,
            "#ccother" : 0,
            "#ccmods" : 0,
            "#ccmusic" : 0,
            "#ccmovie" : 0,
            "#ccevents" : 0,
            "#ccgroup" : 0,
            "#ccbannews" : 0
        }
        noauthor = 0
        creators = {}
        count = 0
        for post in posts['items']:
            if post['date'] > ts:
                count += 1
                if 'created_by' not in post:
                    noauthor += 1
                    continue
                if len(post['text']) > 3:
                    post_hash = post['text'].split()[0]
                    if post_hash in hashs:
                        hashs[post_hash] += 1
                    else:
                        nohash += 1
                if post['created_by'] not in creators:
                    creators[post['created_by']] = 1
                else:
                    creators[post['created_by']] += 1
        
        for moder in moders_days:
            if moder not in creators and moder not in vac:
                moders_days[moder] += 1
                if not test:
                    db.execute(f"UPDATE moders SET days_without_posts = {moders_days[moder]} WHERE vk_id = {moder}")
            else:
                moders_days[moder] = 0
                if not test:
                    db.execute(f"UPDATE moders SET days_without_posts = 0 WHERE vk_id = {moder}")

        for creator in creators:
            if not test:
                db.execute("INSERT OR IGNORE INTO counter(vk_id) VALUES(?)", (creator,))
                db.execute("UPDATE counter SET posts = posts + "+str(creators[creator])+" WHERE vk_id = ?", (creator,))
        con.commit()
        
        #TODO Вывести в чат всю хуйню
        result = "╔══════"+date(time.time(), "%d.%m.%Y")+"══════\n"
        result += f"║ > Всего опубликовано постов [{count}]:\n"
        result +=  "║*********************************\n"

        names = vk.api("users.get", user_ids=','.join(map(str, creators)))
        for name in names:
            result += f"║{name['first_name']} {name['last_name']} - {creators[name['id']]}\n"
        result +=  "║*********************************\n"
                
        result += "║ > Не было постов от: \n"
        result +=  "║*********************************\n"


        not_post_ids = []
        for moder in moders_days:
            if moders_days[moder] != 0:
                not_post_ids.append(moder)

        not_post_names = vk.api("users.get", user_ids=','.join(map(str, not_post_ids)))
        for name in not_post_names:
            result += f"║{name['first_name']} {name['last_name']} - {moders_days[name['id']]}\n"

        result +=  "║*********************************\n"
        result +=  "║ > Статистика модераторов:\n"
        result +=  "║*********************************\n"
        result += f"║Всего модераторов: {len(moders_days)}\n"
        result += f"║Не рабочих: {len(not_post_ids)}\n"
        result += f"║Сегодня делали посты: {len(creators)}\n"
        result += f"║В отпуске: {len(vac)}\n"
        result +=  "║*********************************\n"
        result +=  "║ > Модераторы в отпуске:\n"
        result +=  "║*********************************\n"

        vac_names = vk.api("users.get", user_ids=','.join(map(str, vac)))
        for name in vac_names:
            result += f"║{name['first_name']} {name['last_name']}\n"

        result += "Фильтр постов за сегодня:\n"
        result +=  "║*********************************\n"
        for h in hashs:
            result += f"║{h} - {hashs[h]}\n"
        result += "╚══════════════════"

        vk.api("messages.send", peer_id=peer, message=result)

    def execute(self, vk : VK, peer, **mess):
        userinfo = db.execute("SELECT * FROM admins WHERE vk_id = ?", (mess['from_id'],))
        if len(userinfo.fetchall()) == 1:
            if len(mess['text'].split(' ')) > 1 and mess['text'].split(' ')[1] == "test":
                self.count(vk, config.PEER_ADD_NUM + config.CONVERSATIONS['flood'], True)
            else:
                self.count(vk, config.PEER_ADD_NUM + config.CONVERSATIONS['new'])
        else:
            vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message="[BOT]\nВы не можете использовать эту команду")

if __name__ == "__main__":
    main.count(VK(config.TOKEN), config.PEER_ADD_NUM + config.CONVERSATIONS['new'])