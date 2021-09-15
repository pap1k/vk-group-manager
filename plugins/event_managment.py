from core import VK
from plugins.db import cursor as db, con
import config


class main:
    triggers = ['makeevent', 'dismissevent', 'unevent']
    target = True

    def execute(self, vk : VK, peer, **mess):
        userinfo = db.execute("SELECT * FROM admins WHERE vk_id = ?", (mess['from_id'],))
        if len(userinfo.fetchall()) == 1:
            db.execute("CREATE TABLE IF NOT EXISTS moders(vk_id INT NOT NULL, event INT DEFAULT 0)")

            data = db.execute("SELECT * FROM moders WHERE vk_id = ? AND event = 1", (mess['userId'],)).fetchall()
            
            name = vk.api("users.get", user_ids=mess['userId'])[0]

            #Проверка является ли чел модером вообще
            if len(db.execute("SELECT * FROM moders WHERE vk_id = ?", (mess['userId'],)).fetchall()) == 0:
                return vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message="[BOT]\nУказанный пользователь не является модером")

            #Назначение ивент-модером
            if mess['cmd'] == "makeevent":
                if len(data) == 0:
                    db.execute("UPDATE moders SET event = 1 WHERE vk_id = ?", (mess['userId'],))

                    m = f"[BOT]\n{name['first_name']} {name['last_name']} назначен ивент-модером"

                    r = vk.api("messages.addChatUser", chat_id=config.CONVERSATIONS['events'], user_id=mess['userId'])
                    if not r:
                        m += "\n Ошибка приглашения в Event Chat"

                    vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message=m)
                else:
                    vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message="[BOT]\nУказанный пользователь уже является ивент-модером")

            #Снятие с поста ивент-модера
            else:
                if len(data) > 0:
                    db.execute("UPDATE moders SET event = 0 WHERE vk_id = ?", (mess['userId'],))

                    m = f"[BOT]\n{name['first_name']} {name['last_name']} снят с поста ивент-модера в боте"

                    r = vk.api("messages.removeChatUser", chat_id=config.CONVERSATIONS['events'], user_id=mess['userId'])
                    if not r:
                        m += "\n Ошибка исключения из Event Chat"

                    vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message=m)
                else:
                    vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message="[BOT]\nУказанный пользователь не является ивент-модером")

            con.commit()
        else:
            vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message="[BOT]\nВы не можете использовать эту команду")