from core import LongPoll, VK
from log import Log
import config, sys
from functions import newMessageEventHandler

vk = VK(config.TOKEN)
log = Log("[MAIN]").log

def sendStartAnnounce(text):
    if type(config.CONV_TO_LISTEN) == list:
        vk.api("messages.send", peer_id=config.PEER_ADD_NUM + config.CONV_TO_LISTEN[0], message = text)
    elif type(config.CONV_TO_LISTEN) == int:
        vk.api("messages.send", peer_id=config.PEER_ADD_NUM + config.CONV_TO_LISTEN, message=text)

startinfo = "[BOT]\nЗапускается...."
while True:
    try:
        LP = LongPoll(config.TOKEN, config.GROUP_ID_PROD)

        LP.addListener('message_new', newMessageEventHandler)

        log("Started", createfile=True)
        sendStartAnnounce(startinfo+"\nУспешный запуск")

        LP.run()
    except KeyboardInterrupt:
        break
    except Exception as err:
        sendStartAnnounce(startinfo+"\nОшибка запуска")
        print(f'НЕОТЛОВЛЕННАЯ ОШИБКА {err}')







