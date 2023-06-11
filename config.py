from dotenv import load_dotenv
load_dotenv()
import os
TOKEN = os.getenv("VK_TOKEN")
GROUP_ID_PROD = 145098987
GROUP_ID = 145098987
CMD_SYMBOL = '/'
CONV_TO_LISTEN = 217
# CONV_TO_LISTEN = 198
DB_PATH = "manager.db"
PEER_ADD_NUM = 2000000000
CONVERSATIONS = {
    "events" : 176,
    "flood" : 166,
    "new" : 165
}
# CONVERSATIONS = {
#     "events" : 212,
#     "flood" : 210,
#     "new" : 165
# }