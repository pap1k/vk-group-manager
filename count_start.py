from plugins.count import main
from core import VK
import config

if __name__ == "__main__":
    counter = main()
    try:
        counter().count(VK(config.TOKEN), config.PEER_ADD_NUM + config.CONVERSATIONS['new'])
    except Exception as er:
        print(er)