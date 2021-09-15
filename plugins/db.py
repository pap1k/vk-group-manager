import sqlite3, config

con = sqlite3.connect(config.DB_PATH)

cursor = con.cursor()