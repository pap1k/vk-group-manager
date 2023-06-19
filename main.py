from core import LongPoll, VK
from log import Log
import config, sys
from functions import newMessageEventHandler

vk = VK(config.TOKEN)
log = Log("[MAIN]").log

def sendStartAnnounce(text):
    if type(config.CONV_TO_LISTEN) == list:
        for conv in config.CONV_TO_LISTEN:
            vk.api("messages.send", peer_id=config.PEER_ADD_NUM + conv, message = text)
    elif type(config.CONV_TO_LISTEN) == int:
        vk.api("messages.send", peer_id=config.PEER_ADD_NUM + config.CONV_TO_LISTEN, message=text)

startinfo = "Запускается...."
while True:
    try:
        LP = LongPoll(config.TOKEN)

        LP.addListener('message_new', newMessageEventHandler)

        log("Started", createfile=True)
        sendStartAnnounce(startinfo+"\nУспешный запуск")
        
        LP.run()
    except KeyboardInterrupt:
        break
    except Exception as err:
        sendStartAnnounce(startinfo+"\nОшибка запуска")
        print(f'НЕОТЛОВЛЕННАЯ ОШИБКА {err}')







