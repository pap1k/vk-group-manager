import datetime
from plugins.db import cursor as db
from plugins.db import con
from perms import Perms

def date(unixtime, format = '%d.%m.%Y %H:%M:%S'):
    d = datetime.datetime.fromtimestamp(unixtime)
    return d.strftime(format)

class main:
    triggers = [['elog', 'Показывает подробную статистику отчетов ивент модера на текущий момент']]
    target = False
    perm = Perms.Admin

    def execute(self, cmd, reply, **_):
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
                    reportTable[report[1]]['money'] = moderinfo[0][0]
            print(reportTable)
        else:
            reply("В базе нет ни одного отчета")