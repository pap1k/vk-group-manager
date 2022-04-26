from core import VK, getStrTime
import config, importlib, os, re

vk = VK(config.TOKEN)

plugins = []



def loadCommands():
    for file in os.listdir('plugins'):
        if os.path.isfile('plugins/'+file) and '.py' in file and file not in ['utils.py', 'db.py']:
            plugin = importlib.import_module('plugins.'+file.replace('.py',''))
            if hasattr(plugin.main, "triggers"):
                plugins.append(plugin)
                print(f"{getStrTime()} Загружен плагин "+file.replace('.py',''))
            else: print(f"{getStrTime()} Ошибка загрузки плагина "+file.replace('.py','')+" - отсутствует атрибут triggers")

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
        if not message['text'].startswith(config.CMD_SYMBOL):
            return None

        cmd = message['text'].lower().replace('\n', ' ').split(' ')[0].replace(config.CMD_SYMBOL, '')
        userId = None
        if len(message['text'].split(' ')) >= 2:
            userId = getUserIdFromMentor(message['text'].split(' ')[1])

        for plugin in plugins:
            for trigger in plugin.main.triggers:
                
                cond = cmd == trigger
                if type(trigger) == list:
                    cond = cmd == trigger[0]
                if cond:
                    print(f'{getStrTime()} Словлена команда: {message["text"].lower() }')
                    reply = lambda txt: vk.api("messages.send", peer_id=message['peer_id'], reply_to=message['id'], message="[BOT]\n"+txt)
                    if cmd == "cmdlist":
                        plugin.main().execute(vk, peer = message['peer_id'], plist = plugins, cmd = cmd, **message)
                        return None
                    elif hasattr(plugin.main, 'target') and not userId:
                        vk.api("messages.send", peer_id=message['peer_id'], message='Ошибка: Не указан пользователь (Указывать через @)', reply_to=message['id'])
                        return None
                    plugin.main().execute(vk, peer = message['peer_id'], userId = userId, cmd = cmd, reply=reply, **message)
                    # threading.Thread(target=plug.execute,args=(cmd, userId)).start()
        