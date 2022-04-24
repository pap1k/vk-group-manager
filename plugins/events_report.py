import datetime, time
from core import VK
from plugins.db import cursor as db
from plugins.db import con

def date(unixtime, format = '%d.%m.%Y %H:%M:%S'):
    d = datetime.datetime.fromtimestamp(unixtime)
    return d.strftime(format)

class main:
    triggers = [['report', 'Ивент модеры с помощью нее оставляют отчеты']]
    vkInstanse : VK
    peer = 0
    mess = {}
    def execute(self, vk : VK, peer, **mess):
        self.vkInstanse = vk
        self.peer = peer
        self.mess = mess
        userinfo = db.execute("SELECT * FROM moders WHERE vk_id = ?", (mess['from_id'],)).fetchall()
        if len(userinfo) == 1:
            if userinfo[0][1] == 1:
                msgdata = mess['text'].split('\n')
                if len(msgdata) != 3 or 'attachments' not in mess or len(mess['attachments']) == 0 or mess['attachments'][0]['type'] != 'photo':
                    return self.reply("Отправляйте отчет согласно следующему формату:\n\n/report\n[Сумма выплаченного приза]\n[Ник победителя]\n[Скриншот выплаты]")
                
                msgdata = list(map(str.strip, msgdata))

                if not msgdata[1].isnumeric() or len(msgdata[2]) < 3:
                    return self.reply("Отправляйте отчет согласно следующему формату:\n\n/report\n[Сумма выплаченного приза]\n[Ник победителя]\n[Скриншот выплаты]")
                report_data = {
                    'sum': int(msgdata[1]),
                    'winner': msgdata[2]
                }
                if report_data['sum'] <= 0:
                    return self.reply("Сумма не может быть <= 0")

                if report_data['sum'] > userinfo[0][3]:
                    return self.reply(f"По данным бота у остаток ваших средств - {userinfo[0][3]}, а вы хотите сдать отчет с суммой {report_data['sum']}. Если это ошибка, обратитесь к админам группы.")

                #Получаем ссылку на фотку
                attach = mess['attachments'][0]
                maximum = [0,0]
                idx = 0
                for size in attach['photo']['sizes']:
                    if size['width'] > maximum[0]:
                       maximum = [size['width'], idx]
                    idx+=1
                report_data['photo'] = attach['photo']['sizes'][maximum[1]]['url']
                
                db.execute("INSERT INTO reports(vk_id, prize, winner, date_of_report, photo_url) VALUES(?, ?, ?, ?, ?)", (mess['from_id'], report_data['sum'], report_data['winner'], date(time.time()), report_data['photo']))
                db.execute("UPDATE moders SET money_left = ?", (userinfo[0][3]-report_data['sum'], ))
                self.reply("Отчет сохранен: ${}, {}, {}\nОстаток средств: {}".format(report_data['sum'], report_data['winner'], date(time.time()), userinfo[0][3]-report_data['sum']))
                con.commit()

            else:
                self.reply("Вы не можете использовать эту команду")
        else:
            self.reply("Вы не можете использовать эту команду")

    def reply(self, text):
        return self.vkInstanse.api("messages.send", peer_id=self.peer, reply_to=self.mess['id'], message="[BOT]\n"+text)