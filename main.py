from core import LongPoll
from core import VK, getStrTime
from plugins.count import main
from plugins import month
import config
from functions import newMessageEventHandler
from threading import Thread
import time

vk = VK(config.TOKEN)

def sendMessagess(text):
    if type(config.CONV_TO_LISTEN) == list:
        for conv in config.CONV_TO_LISTEN:
            vk.api("messages.send", peer_id=config.PEER_ADD_NUM + conv, message = text)
    elif type(config.CONV_TO_LISTEN) == int:
        vk.api("messages.send", peer_id=config.PEER_ADD_NUM + config.CONV_TO_LISTEN, message=text)

def loop():
    print(f'{getStrTime()} Запущен таск для отчётов')
    while True:
        time.sleep(0.05)
        current_time = time.localtime()
        if current_time.tm_hour == 0 and current_time.tm_min == 1 and current_time.tm_sec > 0 and current_time.tm_sec < 2:
            print(f'{getStrTime()} Ежедневный отчёт генерируется')
            sendMessagess('[BOT] Ежедневный отчёт генерируется')
            m2 = main()
            m2.count(VK(config.TOKEN), config.PEER_ADD_NUM + config.CONVERSATIONS['new'])
            print(f'{getStrTime()} Ежедневный отчёт отправлен')
            if current_time.tm_mday == 1:
                print(f'{getStrTime()} Ежемесячный отчёт генерируется')
                vk.api("messages.send", peer_id=config.PEER_ADD_NUM + config.CONV_TO_LISTEN, message='[BOT] Ежемесячный отчёт генерируется')
                sendMessagess('[BOT] Ежемесячный отчёт генерируется')
                m3 = month.main()
                if type(config.CONV_TO_LISTEN) == list:
                    for conv in config.CONV_TO_LISTEN:
                        m3.execute(VK(config.TOKEN), config.PEER_ADD_NUM + conv, {'from_id': config.ADMIN_ID, 'id': None})
                elif type(config.CONV_TO_LISTEN) == int:
                    m3.execute(VK(config.TOKEN), config.PEER_ADD_NUM + config.CONV_TO_LISTEN, {'from_id': config.ADMIN_ID, 'id': None})    
                print('Ежемесячный отчёт отправлен')

t = Thread(target=loop)
t.daemon = True
t.start()

LP = LongPoll(config.TOKEN)

LP.addListener('message_new', newMessageEventHandler)

LP.run()







