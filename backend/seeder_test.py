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
# categories insert
cur.execute('INSERT INTO Categories(name, limit_date, order_number) values ("テストカテゴリ1", "2023-07-02 00:00:00", 0)')
cur.execute('INSERT INTO Categories(name, limit_date, order_number) values ("テストカテゴリ2", "2023-07-03 00:00:00", 1)')
cur.execute('INSERT INTO Categories(name, limit_date, order_number) values ("テストカテゴリ3", "2023-07-04 00:00:00", 2)')
cur.execute('INSERT INTO Categories(name, limit_date, order_number) values ("テストカテゴリ4", "2023-07-05 00:00:00", 3)')

# tasks insert
cur.execute('INSERT INTO Tasks(name, category_ID, description, order_number) values ("テストタスク1", 1, "aaaa", 0)')
cur.execute('INSERT INTO Tasks(name, category_ID, description, order_number) values ("テストタスク2", 1, "bbbb", 1)')
cur.execute('INSERT INTO Tasks(name, category_ID, description, order_number) values ("テストタスク3", 2, "cccc", 0)')
cur.execute('INSERT INTO Tasks(name, category_ID, description, order_number) values ("テストタスク4", 3, "dddd", 0)')
cur.execute('INSERT INTO Tasks(name, category_ID, description, order_number) values ("テストタスク5", 1, "eeee", 2)')
cur.execute('INSERT INTO Tasks(name, category_ID, description, order_number) values ("テストタスク6", 3, "ffff", 1)')
cur.execute('INSERT INTO Tasks(name, category_ID, description, order_number) values ("テストタスク7", 4, "gggg", 0)')
cur.execute('INSERT INTO Tasks(name, category_ID, description, order_number) values ("テストタスク8", 2, "hhhh", 1)')

conn.commit()
conn.close()