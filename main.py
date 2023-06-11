from core import LongPoll, VK
from log import Log
import config, sys
from functions import newMessageEventHandler

vk = VK(config.TOKEN)
log = Log("[MAIN]").log

def sendMessagess(text):
    if type(config.CONV_TO_LISTEN) == list:
        for conv in config.CONV_TO_LISTEN:
            vk.api("messages.send", peer_id=config.PEER_ADD_NUM + conv, message = text)
    elif type(config.CONV_TO_LISTEN) == int:
        vk.api("messages.send", peer_id=config.PEER_ADD_NUM + config.CONV_TO_LISTEN, message=text)

if "-count" in sys.argv:
    from plugins.count import main as counter
    try:
        counter().count(vk, config.PEER_ADD_NUM + config.CONVERSATIONS['new'])
    except Exception as er:
        print(er)
        vk.api("messages.send", peer_id=config.PEER_ADD_NUM + config.CONV_TO_LISTEN, message = "Не получилось провести подсчет")
    quit()

while True:
    try:
        LP = LongPoll(config.TOKEN)

        LP.addListener('message_new', newMessageEventHandler)
        log("Started", createfile=True)
        LP.run()
    except KeyboardInterrupt:
        break
    except Exception as err:
        print(f'НЕОТЛОВЛЕННАЯ ОШИБКА {err}')







