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
                    reportTable[report[1]]['spent'] = report[2]
                    reportTable[report[1]]['count'] = 1
                    reportTable[report[1]]['money'] = moderinfo[0][0]
            names = vk.api("users.get", user_ids=','.join(map(str, list(reportTable))))
            c = 0
            for userId in reportTable:
                result += f"[id{userId}|{names[c]['first_name']} {names[c]['last_name']}]:\nВсего потрачено: {reportTable[userId]['spent']}\nВсего отчетов: {reportTable[userId]['count']}\nОстаток средств: {reportTable[userId]['money']}\n\n"

            reply(result)

        else:
            reply("В базе нет ни одного отчета")