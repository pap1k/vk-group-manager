import datetime
from perms import Perms

def date(unixtime, format = '%d.%m.%Y %H:%M:%S'):
    d = datetime.datetime.fromtimestamp(unixtime)
    return d.strftime(format)

class main:
    triggers = [['cmdlist', 'Показывает список всех команд и их описание']]
    perm = Perms.Admin

    def execute(self, reply, plist, **_):
        txt = ""
        for plugin in plist:
            for trigger in plugin.main.triggers:
                if type(trigger) == list:
                    txt += f"[id0|/{trigger[0]}] : {trigger[1]}"
                else:
                    txt += f"[id0|/{trigger}]"
                txt += "\n"
        reply(txt)
        