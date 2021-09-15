from core import LongPoll
import config
from functions import newMessageEventHandler

LP = LongPoll(config.TOKEN)

LP.addListener('message_new', newMessageEventHandler)

LP.run()