from plugins.db import cursor as db
from plugins.db import con
from perms import Perms

class main:
    triggers = [['flushestat', 'Сбрасывает стату ВСЕХ ивентов']]
    confirm = True
    perm = Perms.Admin
    def execute(self, reply, **mess):
        if 'has_confirmation' in mess:
            if mess['has_confirmation'] in ['да', 'yes']:
                db.execute("DELETE FROM reports")
                con.commit()
                reply("Все отчеты удалены")
            else:
                reply("Сбор статистики отменен")
        else:
            reply("Вы действительно хотите сбросить статистику работы всех ивентов? [да/нет]")
