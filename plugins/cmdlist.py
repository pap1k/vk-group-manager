import datetime
from perms import Perms

def date(unixtime, format = '%d.%m.%Y %H:%M:%S'):
    d = datetime.datetime.fromtimestamp(unixtime)
    return d.strftime(format)

class main:
    triggers = [['cmdlist', 'Показывает список всех команд и их описание']]
    perm = Perms.User

    def execute(self, reply, plist, **message):
        txt = ""
        for plugin in plist:
            if Perms.hasPerm(message['from_id'], plugin.main.perm, trigger):
                for trigger in plugin.main.triggers:
                    if type(trigger) == list:
                        txt += f"[id0|/{trigger[0]}] : {trigger[1]}"
                    else:
                        txt += f"[id0|/{trigger}]"
                    txt += "\n"
        if txt == "":
            txt = "У вас нет доступных команд"
        reply(txt)
        