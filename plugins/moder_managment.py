from core import VK
from plugins.db import cursor as db, con
import config, sys


class main:
    triggers = [['addmoder', 'Назначает чела модером в группе и в боте. При использовании админом на самого себя может снять с него админ права в группе (так работает сам вк)'], ['delmoder', 'Снимает чела с поста модера, ивента(если он им был), снимает модерку в группе. На самом себе тоже не надо юзать']]
    target = True

    def execute(self, vk : VK, peer, **mess):
        userinfo = db.execute("SELECT * FROM admins WHERE vk_id = ?", (mess['from_id'],))
        if len(userinfo.fetchall()) == 1:
            db.execute("CREATE TABLE IF NOT EXISTS moders (vk_id INT NOT NULL, event INT DEFAULT 0, days_without_posts INT DEFAULT 0)")

            data = db.execute("SELECT * FROM moders WHERE vk_id = ?", (mess['userId'],)).fetchall()
            
            name = vk.api("users.get", user_ids=mess['userId'])[0]

            managers = vk.api("groups.getMembers", group_id=config.GROUP_ID, filter='managers')
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

                    m = f"[BOT]\n{name['first_name']} {name['last_name']} назначен модером в боте"

                    if not isModer:
                        if not "-dev" in sys.argv:
                            vk.api("groups.editManager", group_id=config.GROUP_ID, user_id=mess['userId'], role="editor")
                        else:
                            m += "[TEST MODE]"
                        m += " и в группе"

                    r = vk.api("messages.addChatUser", chat_id=config.CONVERSATIONS['flood'], user_id=mess['userId'])
                    if not r:
                        m += "\n Ошибка приглашения во Flood Chat"

                    r = vk.api("messages.addChatUser", chat_id=config.CONVERSATIONS['new'], user_id=mess['userId'])
                    if not r:
                        m += "\n Ошибка приглашения в New Chat"

                    vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message=m)
                
                else:
                    vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message="[BOT]\nУказанный пользователь уже является модером")
            #Снятие с поста модера
            else:
                if len(data) > 0:
                    db.execute("DELETE FROM moders WHERE vk_id=?", (mess['userId'],))
                    m = f"[BOT]\n{name['first_name']} {name['last_name']} снят с поста модера в боте"
                    if isModer:
                        if not "-dev" in sys.argv:
                            vk.api("groups.editManager", group_id=config.GROUP_ID, user_id=mess['userId'])
                        else:
                            m += "[TEST MODE]"
                        m += " и в группе"

                    r = vk.api("messages.removeChatUser", chat_id=config.CONVERSATIONS['flood'], user_id=mess['userId'])
                    if not r:
                        m += "\n Ошибка исключения из Flood Chat"
                    r = vk.api("messages.removeChatUser", chat_id=config.CONVERSATIONS['new'], user_id=mess['userId'])
                    if not r:
                        m += "\n Ошибка исключения из New Chat"
                    r = vk.api("messages.removeChatUser", chat_id=config.CONVERSATIONS['events'], user_id=mess['userId'])
                    if not r:
                        m += "\n Ошибка исключения из Event Chat"
                    
                    vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message=m)
                else:
                    vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message="[BOT]\nУказанный пользователь не является модером")

            con.commit()
        else:
            vk.api("messages.send", peer_id=peer, reply_to=mess['id'], message="[BOT]\nВы не можете использовать эту команду")