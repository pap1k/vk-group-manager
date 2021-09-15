from core import VK
import config, importlib, os, re

vk = VK(config.TOKEN)

plugins = []

def loadCommands():
    for file in os.listdir('plugins'):
        if os.path.isfile('plugins/'+file) and '.py' in file and file not in ['utils.py', 'db.py']:
            plugin = importlib.import_module('plugins.'+file.replace('.py',''))
            if hasattr(plugin.main, "triggers"):
                plugins.append(plugin)
                print("Загружен плагин "+file.replace('.py',''))
            else: print("Ошибка загрузки плагина "+file.replace('.py','')+" - отсутствует атрибут triggers")

loadCommands()

def getUserIdFromMentor(txt):
    found_id = re.findall(r"\[id(\d+)\|.+\]", txt)
    if len(found_id) == 1:
        return int(found_id[0])
    return False

def newMessageEventHandler(obj):
    if 'message' in obj:
        message = obj['message']
        if message['peer_id'] != config.PEER_ADD_NUM+config.CONV_TO_LISTEN:
            if config.CONV_TO_LISTEN != 0:
                return None
        if not message['text'].startswith(config.CMD_SYMBOL):
            return None

        cmd = message['text'].lower().split(' ')[0].replace(config.CMD_SYMBOL, '')
        userId = None
        if len(message['text'].split(' ')) >= 2:
            userId = getUserIdFromMentor(message['text'].split(' ')[1])

        for plugin in plugins:
            for trigger in plugin.main.triggers:
                if cmd == trigger:
                    if hasattr(plugin.main, 'target') and not userId:
                        vk.api("messages.send", peer_id=message['peer_id'], message='Ошибка: Не указан пользователь (Указывать через @)', reply_to=message['id'])
                        return None
                    plugin.main().execute(vk, peer = message['peer_id'], userId = userId, cmd = cmd, **message)
                    # threading.Thread(target=plug.execute,args=(cmd, userId)).start()
                        

        