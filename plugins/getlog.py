from plugins.db import cursor as db
import re

class main:
    triggers = [['getlog', 'Скидывает log.txt']]

    def execute(self, _, reply, **mess):
        ainfo = db.execute("SELECT * FROM admins WHERE vk_id = ?", (mess['from_id'],)).fetchall()
        if len(ainfo) > 0:
            txt = open("log.txt", "r", encoding="utf-8").read().split('\n')
            text = '\n'.join(txt[-30:])
            words = mess['text'].split(" ")
            if len(words) > 1:
                if words[1].isnumeric():
                    text = '\n'.join(txt[-int(words[1]):])
                else:
                    r = re.findall(r"(\d+)-(\d+)", words[1])
                    if len(r[0]) > 0:
                        if r[0][0].isnumeric() and r[0][1].isnumeric():
                            text = '\n'.join(txt[int(r[0][0]):int(r[0][1])])
                        else:
                            reply("Юзаж: /getlog без параметров - последние 30, /getlog n - последние n, /getlog n-n1 - с n по n1")
                    else:
                        reply("Юзаж: /getlog без параметров - последние 30, /getlog n - последние n, /getlog n-n1 - с n по n1")
            
            reply(text)
        else: reply("Вы не можете использовать эту команду")