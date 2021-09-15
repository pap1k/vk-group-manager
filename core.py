import requests
from random import randint as rand

CORE_V = 0.3

API_URL = "https://api.vk.com/method/"
API_V = 5.103

def userToGroupEvent(eId):
    table = {
        4: "message_new",
        5: "message_edit"
    }
    return table[eId] if eId in table else "Unknown"

class VK:
    token : str
    v : float
    lang : str

    def __init__(self, token : str, v = API_V, lang = "ru") -> None:
        self.lang = lang
        self.token = token
        self.v = v

    def api(self, method, **params):

        params['access_token'] = self.token
        params['v'] = self.v
        params['lang'] = self.lang

        if method == "messages.send":
            params['random_id'] = rand(1000, 100000)

        r = requests.post(API_URL+method, data=params).json()
        if 'error' in r:
            print("An error: ", r['error'])
            return None
        else:
            return r['response']


class LongPoll:
    key : str
    ts : int
    server : str
    wait : int
    vkInstanse : VK
    doFlag = True
    group_id : int
    listeners : list
    mode : str

    def __init__(self, vk, group_id = 0, wait = 20) -> None:
        if type(vk) == VK:
            self.vkInstanse = vk
        else:
            self.vkInstanse = VK(vk)
        self.listeners = []
        self.group_id = group_id
        self.wait = wait
        self.getServerInfo()

    def getServerInfo(self):
        if self.group_id != 0:
            info = self.vkInstanse.api("groups.getLongPollServer", group_id=self.group_id)
            self.mode = "group"
        else:
            info = self.vkInstanse.api("messages.getLongPollServer")
            self.mode = "user"

        self.key = info['key']
        self.ts = info['ts']
        self.server = info['server'] if "https" in info['server'] else 'https://'+info['server']

    def addListener(self, event, listener):
        self.listeners.append([event, listener])

    def run(self):
        self.doFlag = True
        first = True
        while self.doFlag:
            try:
                if first:
                    print("Бот слушает обновления")
                    first = False

                resp = requests.get(f"{self.server}?act=a_check&key={self.key}&ts={self.ts}&wait={self.wait}").json()
                if 'failed' in resp:
                    if resp['failed'] == 1:
                        self.ts = resp['ts']
                        continue
                    elif resp['failed'] == 2 or resp['failed'] == 3:
                        self.getServerInfo()
                        continue
                    elif resp['filed'] == 4:
                        continue
                    else:
                        print("Unknown erorr")
                        self.getServerInfo()
                        continue
                if resp['ts'] != self.ts:
                    self.ts = resp['ts']
                for upd in resp['updates']:
                    for listener in self.listeners:
                        event = upd['type'] if self.mode == "group" else userToGroupEvent(upd[0])
                        if listener[0] == event:
                            if self.mode == "user":
                                #КОСТЫЛЬ ТОЛЬКО НА СООБЩЕНИЯ КОТОРЫЕ ЧЕРЕЗ ЮЗЕР ЛОНГПОЛЛ
                                mess = self.vkInstanse.api("messages.getById", message_ids=upd[1])['items'][0]
                                obj = {'message': mess}
                                listener[1](obj)
                                # threading.Thread(target=listener[1], args=(obj,)).start()
                            else:
                                # threading.Thread(target=listener[1], args=(upd['object'],)).start()
                                listener[1](upd['object'])
                                        
            except KeyboardInterrupt:
                self.stop()

            # except Exception as e:
            #     print("Uncatchable exception: ", e)

    def stop(self):
        print("Stopping LongPoll")
        self.doFlag = False

        