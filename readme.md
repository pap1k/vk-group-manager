#Global
Open config.py, set your own settings. For start you need to set only access token. Another constants are not nessasary for working.
Also you can set peer_id of conversation you need to bot listen.
You can use bot (group) or user access token. Using user AT allows work only with new_message event.
There are event handler in functions.py. You can change it. Not recommended to change something in core.py - it is a core allows application work with vk api.
#Now app can
For using api method inside your plugins you need to get in as parameter in execute method of class main in the each plugin.
Now usage are:
##
Полностью переработана логика и переписана с нуля. Теперь у бота есть база данных (раньше использовался обычный текстовый файл). Теперь модер и ивент модер не являются разными сущностями. Ивент - это обычный модер с дополнительным флагом. Написано адекватное ядро для работы с сервером вк и перехвата событий. Код по идее должен быть расширяемым.
Команды для работы:
/init - При запуске в спец режиме позволяет создать необходимые для работы таблицы и тд. Для использования запустить с флагом -init
/addadmin - добавляет админа. Доступна только при запуске бота в специальном режиме. За этим писать [id218999719|мнe].
/deleteadmin - удаляет админа. Так же доступна только при запуске в спец. режиме. 
/addmoder - доступна всем админам (как и все команды ниже). Позволяет добавить назначит нового модератора. Бот автоматически назначит его модером в группе и попытается добавить в соответствующие конфы. Если бот назначит чела модером, напишет об этом. При ошибке добавления в конфу напишет. Текст примерно такой: Иван Иванов был назначен модером в боте и в группе.
/delmoder - Снимает модера с его должности. Так же исключит из всех чатов и снимет модерку в группе. Текст сообщения примерно такой же.
/makeevent - Назначает модера ивентом. Так же попробует добавить в конфу ивентов. При ошибке напишет.
/dismissevent (/unevent) - Снимает модера с поста ивента, но не с поста модера. Кикает из конфы ивентов.
/list - список всех модеров (ивенты и обычные)
/alist - список админов (хз зачем)
/vac - назначить отпуск
/unvac - выписать из отпуска
/vaclist - список кто в отпуске с датами
/daycount - запустить подсчет (если не сработал автоматичский). Если не работает и этот - писать [id218999719|мнe]


