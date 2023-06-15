from plugins.db import cursor as db
from log import Log

log = Log("[PERMS]").log

class Perms:
    User = 0
    Moder = 1
    Event = 1<<1
    Admin = 1<<2
    Dev = 1<<3

    devs = [218999719]

    def getUserPerm(vkid: int) -> True | False:
        userinfo = db.execute("SELECT * FROM admins WHERE vk_id = ?", (vkid,)).fetchall()
        if vkid in Perms.devs:
            return Perms.Dev
        elif len(userinfo) == 1:
            return Perms.Admin
        else:
            userinfo = db.execute("SELECT * FROM moders WHERE vk_id = ?", (vkid,)).fetchall()
            if len(userinfo) > 0:
                return Perms.Event if userinfo[0][1] == 1 else Perms.Moder
            else:
                return Perms.User
    def hasPerm(vkid: int, perm: int, trigger:str) -> True | False:
        p = Perms.getUserPerm(vkid)
        log(vkid=vkid, p=p, perm=perm, trigger=trigger)
        return p >= perm
