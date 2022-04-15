from core import VK
import sys
from plugins.db import cursor as db, con


class main:
    triggers = ['addadmin', 'deleteadmin']
    target = True
    def execute(self, vk : VK, peer : int, **mess):

        if "-dev" in sys.argv:
            db.execute("CREATE TABLE IF NOT EXISTS admins (vk_id INT NOT NULL)")

            data = db.execute("SELECT * FROM admins WHERE vk_id = ?", (mess['userId'],))

            if mess['cmd'] == "addadmin":
                if len(data.fetchall()) == 0:
                    db.execute("INSERT INTO admins(vk_id) VALUES(?)", (mess['userId'],))

                    name = vk.api("users.get", user_ids=mess['userId'])[0]

                    m = f"[BOT]\n{name['first_name']} {name['last_name']} назначен админом в боте"
                    vk.api("messages.send", peer_id=peer, message=m, reply_to=mess['id'])
                else:
                    vk.api("messages.send", peer_id=peer, message="[BOT]\nУказанный пользователь уже админ", reply_to=mess['id'])
            else:
                if len(data.fetchall()) > 0:
                    db.execute("DELETE FROM admins WHERE vk_id = ?", (mess['userId'],))

                    name = vk.api("users.get", user_ids=mess['userId'])[0]

                    m = f"[BOT]\n{name['first_name']} {name['last_name']} снят с поста админа в боте"
                    vk.api("messages.send", peer_id=peer, message=m, reply_to=mess['id'])
                else:
                     vk.api("messages.send", peer_id=peer, message="[BOT]\nУказанный пользователь не админ", reply_to=mess['id'])

            con.commit()
            
        else:
            vk.api("messages.send", peer_id=peer, message="[BOT]\nДля использования этой команды необходимо запустить программу в режиме -dev", reply_to=mess['id'])