import datetime
from plugins.db import cursor as db
from plugins.db import con
from perms import Perms

def date(unixtime, format = '%d.%m.%Y %H:%M:%S'):
    d = datetime.datetime.fromtimestamp(unixtime)
    return d.strftime(format)

class main:
    triggers = [['estat', 'Показывает подробную статистику отчетов ивент модера на текущий момент'], ['eventstat', 'Аналог'], ['flushestatid', 'Сбрасывает стату отдельного ивента']]
    target = True
    perm = Perms.Admin

    def execute(self, userId, cmd, reply, **_):
        eventinfo = db.execute("SELECT * FROM reports WHERE vk_id = ?", (userId,)).fetchall()
        moderinfo = db.execute("SELECT money_left FROM moders WHERE vk_id = ?", (userId,)).fetchall()
        if len(eventinfo) > 0:
            #stat
            if cmd == self.triggers[0][0] or cmd == self.triggers[1][0]:
                reporttext = "Список отчетов модера:\n"
                spent = 0
                for row in eventinfo:
                    reporttext += f"[{row[0]}]{row[4]} -- {row[2]} -> {row[3]}\n{row[5]}\n"
                    spent += row[2]#prize
                reporttext += f"\nВсего потрачено: {spent}\nВсего отчетов: {len(eventinfo)}\nОстаток средств: {moderinfo[0][0]}"
                reply(reporttext)
            #flush id
            else:
                db.execute("DELETE FROM reports WHERE vk_id = ?", (userId,))
                con.commit()
                reply("Все отчеты модера удалены")
        else:
            reply("По данным бота, указанный модер не сдал ни одного отчета. Остаток средств: "+str(moderinfo[0][0]))