from core import VK
from log import Log
import config, importlib, os, re, argparser
from perms import Perms

vk = VK(config.TOKEN)
vk_user = VK(config.USER_TOKEN)

conf = {'v': "питон ты долбоеб че за костыли нахуй"}
yesno = ["да", "yes", "no", "нет"]

plugins = []

log = Log("[FUNCS]").log

def loadCommands():
    for file in os.listdir('plugins'):
        if os.path.isfile('plugins/'+file) and '.py' in file and file not in ['utils.py', 'db.py']:
            plugin = importlib.import_module('plugins.'+file.replace('.py',''))
            if hasattr(plugin.main, "triggers"):
                if not hasattr(plugin.main, "perm"):
                    log(f"[WARN]Plugin {file.replace('.py','')} doesnt have PERM attribute")
                plugins.append(plugin)
                log(f"Загружен плагин "+file.replace('.py',''))
            else: log(f"Ошибка загрузки плагина "+file.replace('.py','')+" - отсутствует атрибут triggers")

loadCommands()

def getUserIdFromMentor(txt):
    found_id = re.findall(r"\[id(\d+)\|.+\]", txt)
    if len(found_id) == 1:
        return int(found_id[0])
    return False

def newMessageEventHandler(obj):
    if 'message' in obj:
        message = obj['message']
        if type(config.CONV_TO_LISTEN) == list:
            if message['peer_id'] not in [c+config.PEER_ADD_NUM for c in config.CONV_TO_LISTEN]:
                if config.CONV_TO_LISTEN != []:
                    return None
        else:
            if message['peer_id'] != config.PEER_ADD_NUM+config.CONV_TO_LISTEN:
                if config.CONV_TO_LISTEN != 0:
                    return None
        if not message['text'].startswith(config.CMD_SYMBOL) and not message['text'].lower() in yesno:
            return None

        cmd = message['text'].lower().replace('\n', ' ').split(' ')[0].replace(config.CMD_SYMBOL, '')
        if cmd in yesno:
            if 'execute' in conf['v']:
                p = conf['v']['params']
                p['message']['has_confirmation'] = cmd
                conf['v']['execute'].main().execute(vk = vk, peer = p['peer'], userId = p['userId'], cmd = p['cmd'], reply = p['reply'], **p['message'])
                conf['v'] = "питонр ты просто пиздец даун я хуею"
                return None

        userId = None
        if len(message['text'].split(' ')) >= 2:
            userId = getUserIdFromMentor(message['text'].split(' ')[1])

        for plugin in plugins:
            for trigger in plugin.main.triggers:
                
                arglist = []
                cond = cmd == trigger
                if type(trigger) == list:
                    cond = cmd == trigger[0]
                if cond:
                    log(f'Словлена команда: {message["text"].lower() }')
                    reply = lambda txt: vk.api("messages.send", peer_id=message['peer_id'], reply_to=message['id'], message="[BOT]\n"+txt)
                    if hasattr(plugin.main, 'perm'):
                        if not Perms.hasPerm(message['from_id'], plugin.main.perm, trigger):
                            return reply("Вы не можете использовать эту команду (perms)")
                    if cmd == "cmdlist":
                        plugin.main().execute(vk = vk, peer = message['peer_id'], plist = plugins, reply = reply, cmd = cmd, uservk = vk_user, **message)
                        return None
                    elif hasattr(plugin.main, 'target') and not userId:
                        vk.api("messages.send", peer_id=message['peer_id'], message='Ошибка: Не указан пользователь (Указывать через @)', reply_to=message['id'])
                        return None
                    elif hasattr(plugin.main, 'confirm'):
                        conf['v'] = {'execute': plugin, 'params': {'peer': message['peer_id'], 'userId': userId, 'cmd' : cmd, 'reply':reply, 'message': message, 'arglist': arglist, 'uservk': vk_user}}
                    elif hasattr(plugin.main, 'arglist'):
                        res, args = argparser.parse(message['text'], plugin.main.arglist)
                        if not res:
                            err = ""
                            for i in range(len(plugin.main.arglist)):
                                if args[i] == None:
                                    err += f"Параметр {i+1} ожидается как {plugin.main.arglist[i]}\n"
                            if hasattr(plugin.main, 'hint'):
                                err += "\n\n"+plugin.main.hint
                            vk.api("messages.send", peer_id=message['peer_id'], message='Ошибка в наборе параметров:\n'+err, reply_to=message['id'])
                            return None
                        else:
                            arglist = args
                    plugin.main().execute(vk = vk, peer = message['peer_id'], userId = userId, cmd = cmd, reply=reply, arglist=arglist, uservk = vk_user, **message)
        