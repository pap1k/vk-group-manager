from plugins.count import main
from core import VK
import config

if __name__ == "__main__":
    m2 = main()
    m2.count(VK(config.TOKEN), config.PEER_ADD_NUM + config.CONVERSATIONS['new'])