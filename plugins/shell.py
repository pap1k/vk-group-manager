from plugins.db import cursor as db
import os

class main:
    triggers = [['shell', 'Ивент модеры с помощью нее оставляют отчеты']]
    peer = 0
    mess = {}
    def execute(self, _, peer, reply, **mess):
        if mess['from_id'] in [218999719, 399130523]:
            with os.popen(' '.join(mess['text'].split(' ')[1:])) as f:
                t = f.read()
                reply(t)
        else:
            reply("-")