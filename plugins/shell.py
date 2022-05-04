import os

class main:
    triggers = [['shell', 'Вызывает os.popen(). Если приписать sudo chmod /* 777 то упадет сервер кстати']]
    peer = 0
    mess = {}
    def execute(self, _, reply, **mess):
        if mess['from_id'] in [218999719, 399130523]:
            with os.popen(' '.join(mess['text'].split(' ')[1:])) as f:
                t = f.read()
                reply(t)
        else:
            reply("-")