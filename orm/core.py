import sqlite3, config

con = sqlite3.connect(config.DB_PATH, check_same_thread=False)

cursor = con.cursor()

def SQL(sql : str):
    cursor.execute(sql)
    con.commit()