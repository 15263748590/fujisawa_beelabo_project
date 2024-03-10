import sqlite3
from typing import Any, List

DATABASE_NAME = 'TODO_APP.db'

class Database:
    @staticmethod
    def execute_SQL(command: str, *args: Any) -> List[Any]:
        conn = sqlite3.connect(DATABASE_NAME)
        cur = conn.cursor()
        cur.execute(command, args)
        if 'SELECT' in command:
            res = cur.fetchall()
        else:
            res = None
            conn.commit()
        cur.close()
        conn.close()
        return res