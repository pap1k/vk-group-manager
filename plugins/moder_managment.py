from core import VK
from plugins.db import cursor as db, con
import config, sys
from perms import Perms

class main:
    triggers = [['addmoder', 'Назначает чела модером в группе и в боте. При использовании админом на самого себя может снять с него админ права в группе (так работает сам вк)'], ['delmoder', 'Снимает чела с поста модера, ивента(если он им был), снимает модерку в группе. На самом себе тоже не надо юзать']]
    target = True
    perm = Perms.Admin
    def execute(self, vk : VK, uservk: VK, peer, reply, **mess):
        db.execute("CREATE TABLE IF NOT EXISTS moders (vk_id INT NOT NULL, event INT DEFAULT 0, days_without_posts INT DEFAULT 0)")

        data = db.execute("SELECT * FROM moders WHERE vk_id = ?", (mess['userId'],)).fetchall()
        
        name = vk.api("users.get", user_ids=mess['userId'])[0]

        managers = uservk.api("groups.getMembers", group_id=config.GROUP_ID, filter='managers')
        found = False
        
        for manager in managers['items']:
            if manager['id'] == mess['userId'] and manager['role'] == 'editor': #блок снятия других админов админами через бота, только вручную
                found = True
                break

        isModer = found
        #Назначение модером
        if mess['cmd'] == "addmoder":
            if len(data) == 0:
                db.execute("INSERT INTO moders(vk_id) VALUES(?)", (mess['userId'],))

                m = f"{name['first_name']} {name['last_name']} назначен модером в боте"

                if not isModer:
                    if not "-dev" in sys.argv:
                        uservk.api("groups.editManager", group_id=config.GROUP_ID, user_id=mess['userId'], role="editor")
                    else:
                        m += "[TEST MODE]"
                    m += " и в группе"

                r = uservk.api("messages.addChatUser", chat_id=config.CONVERSATIONS_USER['flood'], user_id=mess['userId'])
                if not r:
                    m += "\n Ошибка приглашения во Flood Chat"

                r = uservk.api("messages.addChatUser", chat_id=config.CONVERSATIONS_USER['new'], user_id=mess['userId'])
                if not r:
                    m += "\n Ошибка приглашения в New Chat"

                reply(m)
            
            else:
                reply("Указанный пользователь уже является модером")

        #Снятие с поста модера
        else:
            if len(data) > 0:
                db.execute("DELETE FROM moders WHERE vk_id=?", (mess['userId'],))
                m = f"{name['first_name']} {name['last_name']} снят с поста модера в боте"
                if isModer:
                    if not "-dev" in sys.argv:
                        uservk.api("groups.editManager", group_id=config.GROUP_ID, user_id=mess['userId'])
                    else:
                        m += "[TEST MODE]"
                    m += " и в группе"

                r = uservk.api("messages.removeChatUser", chat_id=config.CONVERSATIONS_USER['flood'], user_id=mess['userId'])
                if not r:
                    m += "\n Ошибка исключения из Flood Chat"
                r = uservk.api("messages.removeChatUser", chat_id=config.CONVERSATIONS_USER['new'], user_id=mess['userId'])
                if not r:
                    m += "\n Ошибка исключения из New Chat"
                
                reply(m)
            else:
                reply("Указанный пользователь не является модером")

        con.commit()
