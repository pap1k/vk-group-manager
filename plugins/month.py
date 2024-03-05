from core import VK
from plugins.db import cursor as db
from perms import Perms
import argparser
import json, datetime, time, requests

def date(unixtime, format = '%d.%m.%Y %H:%M:%S'):
    d = datetime.datetime.fromtimestamp(unixtime)
    return d.strftime(format)

def alg(elem):
    return elem[1]

def findModer(moders, id):
    for moder in moders:
        if int(moder[0]) == id:
            return moder
    return None

def getModerNick(vk_id, moders):
    moder = findModer(moders, int(vk_id))
    if moder and moder[5] != None:
        return moder[5]
    else:
        return "Не указан ник - vk id: "+str(vk_id)

def getPostCase(num):
    if str(num)[-1] == "1": return "пост"
    elif int(str(num)[-1]) in range(5,10) or str(num)[-1] == "0": return "постов"
    else: return "поста"

def isModerAdmin(id, admins):
    for admin in admins:
        if admin[0] == int(id):
            return True
    return False

class main:
    triggers = [['stat', 'Формирует отчет по работе модеров с момента последней чистки через /flush.']]
    perm = Perms.Admin
    hint = '/stat [зп за каждые 10 постов] [зп за < 10 постов] [зп за 1 проведеннео мп] [до стольки пополнить баланс ивентам. 0 если не пополнять]'
    #stat [зп за каждые 10 постов] [зп за < 10 постов] [зп за 1 проведеннео мп] [до стольки пополнить баланс ивентам. 0 если не пополнять]
    arglist = [argparser.POSITIVE_NUMBER, argparser.POSITIVE_NUMBER, argparser.POSITIVE_NUMBER, argparser.POSITIVE_NUMBER]
    def execute(self, vk : VK, reply, arglist, **message):
        reportmsg = "Выплаты за работу\n\n"
        payments = {}

        moders = db.execute("SELECT * FROM moders").fetchall()

        admins = db.execute("SELECT * FROM admins").fetchall()

        #Подсчет за посты
        reportmsg += "За количество постов:\n"
        counter = db.execute("SELECT * FROM counter").fetchall()
        counter.sort(reverse=True, key=alg)
        ids = [str(i[0]) for i in counter]
        names = vk.api("users.get", user_ids=",".join(ids))

        for i in range(len(counter)):
            if isModerAdmin(counter[i][0], admins):
                continue
            posts = int(counter[i][1])
            zp_per_10 = posts//10 * arglist[0]
            zp = arglist[1]*posts if zp_per_10 == 0 else zp_per_10
            if zp != 0:
                nick = getModerNick(counter[i][0], moders)
                reportmsg += f"{names[i]['first_name']} {names[i]['last_name']}({nick}): {posts} {getPostCase(posts)} -> {zp}$\n"
                if nick not in payments:
                    payments[nick] = zp
                else:
                    payments[nick] += zp

        #подсчет за ивенты
        reportmsg += "\nЗа проведение мп:\n"
        reports = db.execute("SELECT * FROM reports").fetchall()

        reportTable = {}

        if len(reports) > 0:
            for report in reports:
                if report[1] in reportTable:
                    reportTable[report[1]]['spent'] += report[2]
                    reportTable[report[1]]['count'] += 1
                else:
                    reportTable[report[1]] = {}
                    reportTable[report[1]]['spent'] = report[2]
                    reportTable[report[1]]['count'] = 1
        
        names = vk.api("users.get", user_ids=','.join(map(str, list(reportTable))))
        c = 0
        for userId in reportTable:
            if isModerAdmin(userId, admins):
                continue
            zp = reportTable[userId]['count'] * arglist[2]
            nick = getModerNick(userId, moders)
            reportmsg+= f"{names[c]['first_name']} {names[c]['last_name']}({nick}): {reportTable[userId]['count']} мп -> {zp}$"
            if arglist[3] != 0:
                refill = arglist[3] - reportTable[userId]['spent']
                if refill > 0:
                    reportmsg+= f"; докинуть {refill}$"
                    zp += refill
            if zp > 0:
                if nick not in payments:
                    payments[nick] = zp
                else:
                    payments[nick] += zp
            reportmsg+= "\n"
            c+=1

        mydate = date(time.time()-500, "%d_%m_%Y")
        fname = ".\\reports\\report"+mydate+".json"
        with open(fname, "w", encoding="utf-8") as f:
            f.write(json.dumps(
                {
                    "_file": "adminstatfile",
                    "data": payments
                }
            ))
        reply(reportmsg)
        server = vk.api("docs.getMessagesUploadServer", type="doc", peer_id=message['peer_id'])['upload_url']
        file = requests.post(server, files={'file':(fname, open(fname, 'rb'), 'multipart/form-data')}).json()
        doc = vk.api("docs.save", file=file['file'])['doc']
        attach = f"doc{doc['owner_id']}_{doc['id']}"
        vk.api("messages.send", peer_id=message['peer_id'], attachment=attach)
