import config, re

NUMBER = "ЧИСЛО"
POSITIVE_NUMBER = "ПОЛОЖИТЕЛЬНОЕ ЧИСЛО"
STRING = "СТРОКА"
USER = "@ПОЛЬЗОВАТЕЛЬ"

def getUserIdFromMentor(txt):
    found_id = re.findall(r"\[id(\d+)\|.+\]", txt)
    if len(found_id) == 1:
        return int(found_id[0])
    return False

def parse(message : str, arglist : list) -> tuple[bool, list]:
    message = message.replace('  ', ' ')
    if message.startswith(config.CMD_SYMBOL):
        params = message.split(' ')[1:]
    else:
        params = message.split(' ')

    toreturn = [None] * len(arglist)
    for i in range(len(arglist)):
        if arglist[i] == NUMBER:
            if params[i].isnumeric():
                toreturn[i] = int(params[i])
            else:
                toreturn[i] = None
        elif arglist[i] == POSITIVE_NUMBER:
            if params[i].isnumeric() and int(params[i]) >= 0:
                toreturn[i] = int(params[i])
            else:
                toreturn[i] = None
        elif arglist[i] == STRING:
            if params[i] != " ":
                  toreturn[i] = params[i]
            else:
                toreturn[i] = None
        elif arglist[i] == USER:
            id = getUserIdFromMentor(params[i])
            if id:
                toreturn[i] = id
            else:
                toreturn[i] = None

        else:
            return None
    try:
        toreturn.index(None)
        return False, toreturn
    except ValueError:
        return True, toreturn 