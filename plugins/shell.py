import os
from perms import Perms

class main:
    triggers = [['shell', 'Вызывает os.popen(). Если приписать sudo chmod /* 777 то упадет сервер кстати']]
    peer = 0
    mess = {}
    perm = Perms.Dev
    def execute(self, reply, **mess):
        with os.popen(' '.join(mess['text'].split(' ')[1:])) as f:
            t = f.read()
            reply(t)