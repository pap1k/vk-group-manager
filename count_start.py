from plugins.count import main
from core import VK
import config

if __name__ == "__main__":
    try:
        main().count(VK(config.TOKEN), VK(config.USER_TOKEN), config.PEER_ADD_NUM + config.CONVERSATIONS['new'])
    except Exception as er:
        print(er)