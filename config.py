from dotenv import load_dotenv
load_dotenv()
import os
TOKEN = os.getenv("VK_TOKEN_GROUP")
USER_TOKEN=os.getenv("VK_TOKEN_USER")
GROUP_ID_PROD = 145098987
GROUP_ID = 145098987
CMD_SYMBOL = '/'
CONV_TO_LISTEN = [3, 4]
# CONV_TO_LISTEN = 198
DB_PATH = "manager.db"
PEER_ADD_NUM = 2000000000
CONVERSATIONS = {
    "events" : 231,
    "flood" : 4,
    "new" : 2
}
CONVERSATIONS_USER = {
    "events" : 231,
    "flood" : 231,
    "new" : 230
}
# CONVERSATIONS = {
#     "events" : 212,
#     "flood" : 210,
#     "new" : 165
# }