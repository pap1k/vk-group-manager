import datetime
from core import VK
from plugins.db import cursor as db
from plugins.db import con
from perms import Perms

def date(unixtime, format = '%d.%m.%Y %H:%M:%S'):
    d = datetime.datetime.fromtimestamp(unixtime)
    return d.strftime(format)

class main:
    triggers = [['elog', 'Показывает общий лог работы всех ивентов']]
    perm = Perms.Admin

    def execute(self, vk : VK, cmd, reply, **_):
        reports = db.execute("SELECT * FROM reports").fetchall()
        result = "Краткий отчет по всем модерам:\n"

        reportTable = {}

        if len(reports) > 0:
            for report in reports:
                if report[1] in reportTable:
                    reportTable[report[1]]['spent'] += report[2]
                    reportTable[report[1]]['count'] += 1
                else:
                    moderinfo = db.execute("SELECT money_left FROM moders WHERE vk_id = ?", (report[1],)).fetchall()
                    reportTable[report[1]] = {}
                    reportTable[report[1]]['money'] = "0 (не является модером)" if len(moderinfo) == 0 else moderinfo[0][0]
                    reportTable[report[1]]['spent'] = report[2]
                    reportTable[report[1]]['count'] = 1
            names = vk.api("users.get", user_ids=','.join(map(str, list(reportTable))))
            c = 0
            for userId in reportTable:
                result += f"[id{userId}|{names[c]['first_name']} {names[c]['last_name']}]:\n>> Всего потрачено: {reportTable[userId]['spent']}\n>> Всего отчетов: {reportTable[userId]['count']}\n>> Остаток средств: {reportTable[userId]['money']}\n=================\n\n"
                c+=1

            reply(result)

        else:
            reply("В базе нет ни одного отчета")