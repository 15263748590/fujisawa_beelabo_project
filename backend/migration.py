import sqlite3

dbname = 'TODO_APP.db'
conn = sqlite3.connect(dbname)

cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Categories (
                   ID           INTEGER          PRIMARY KEY AUTOINCREMENT,
                   name         VARCHAR(255)     NOT NULL,
                   description  TEXT             DEFAULT '',
                   limit_date   DATETIME,
                   order_number INTEGER,
                   deleted_at   DATETIME         DEFAULT NULL
               )''')

cur.execute('''CREATE TABLE IF NOT EXISTS Tasks(
                   ID           INTEGER          PRIMARY KEY AUTOINCREMENT,
                   name         VARCHAR(255)     NOT NULL,
                   category_ID  INTEGER,
                   description  TEXT             DEFAULT '',
                   status       TINYINT          DEFAULT '0',
                   order_number INTEGER,
                   deleted_at   DATETIME         DEFAULT NULL
               )''')

conn.commit()
conn.close()