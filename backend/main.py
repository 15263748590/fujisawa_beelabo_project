from datetime import datetime

from typing import Optional

from enum import Enum, IntEnum

import sqlite3

from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

DATABASE_NAME = 'TODO_APP.db'
    
def execute_SQL(command, *args):
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

category_keys = ('id', 'name', 'description', 'limit_date', 'order_number', 'deleted_at')

task_keys = ('id', 'name', 'category_id', 'description', 'status', 'order_number', 'deleted_at')

class Category(BaseModel):
    id: int
    name: str
    description: Optional[str] = ""
    limit_date: datetime
    order_number: int
    deleted_at: Optional[datetime] = None

class Task(BaseModel):
    id: int
    name: str
    category_id: int
    description: Optional[str] = ""
    status: int
    order_number: int
    deleted_at: Optional[datetime] = None

class ErrorCode(Enum):
    NOT_NUMBER = "リクエストされた値は数値型である必要があります"
    NOT_TEXT = "リクエストされた値は文字列型である必要があります"
    NOT_DATE = "リクエストされた値は日時型として読み込めません"
    ID_NOT_FOUND = "リクエストされたIDは存在しません"
    STATUS_NOT_FOUND = "リクエストされた数値に対応する達成度はありません"
    MINUS_NUMBER = "マイナスの数値は無効です"
    BAD_TEXT = "空の文字列は無効です"
    DATE_OVER = "現在より前の日時は無効です"
    EDIT_CATEGORY_ID = "カテゴリIDは編集できません"
    EDIT_DELETED_AT = "PUT通信で削除フラグは編集できません"

class TaskStatus(IntEnum):
    NOT_STARTED = 0
    IN_PROGRESS = 1
    DONE = 2

def check_id_categories(id: int):
    category = execute_SQL('SELECT * FROM Categories WHERE ID = ?', id)
    if category == []:
        return True
    if [i[5] for i in category if i[-1] is None] == []:
        return True
    return False

def check_id_tasks(id: int):
    task = execute_SQL('SELECT * FROM Tasks WHERE ID = ?', id)
    if task == []:
        return True
    if [i[6] for i in task if i[-1] is None] == []:
        return True
    return False

def check_category(category: Category):
    if not isinstance(category.id, int):
        return ErrorCode.NOT_NUMBER
    if not category.id >= 0:
        return ErrorCode.ID_NOT_FOUND
    
    if not isinstance(category.name, str):
        return ErrorCode.NOT_TEXT
    if not len(category.name) > 0:
        return ErrorCode.BAD_TEXT
    
    if not isinstance(category.limit_date, datetime):
        return ErrorCode.NOT_DATE
    if not category.limit_date > datetime.now().astimezone():
        return ErrorCode.DATE_OVER

    if not isinstance(category.order_number, int):
        return ErrorCode.NOT_NUMBER
    if not category.order_number >= 0:
        return ErrorCode.MINUS_NUMBER
    
    if category.deleted_at is not None:
        return ErrorCode.EDIT_DELETED_AT
    return 0

def check_task(task: Task):
    if not isinstance(task.id, int):
        return ErrorCode.NOT_NUMBER
    if not task.id >= 0:
        return ErrorCode.ID_NOT_FOUND
    
    if not isinstance(task.name, str):
        return ErrorCode.NOT_TEXT
    if not len(task.name) > 0:
        return ErrorCode.BAD_TEXT
    
    if not isinstance(task.category_id, int):
        return ErrorCode.NOT_NUMBER
    if not task.category_id > 0:
        return ErrorCode.MINUS_NUMBER
    if check_id_categories(task.category_id):
        return ErrorCode.ID_NOT_FOUND
    
    if not isinstance(task.description, str):
        return ErrorCode.NOT_TEXT
    
    if not isinstance(task.status, int):
        return ErrorCode.NOT_NUMBER
    if not (task.status >= 0 and task.status < 3):
        return ErrorCode.STATUS_NOT_FOUND
    
    if not isinstance(task.order_number, int):
        return ErrorCode.NOT_NUMBER
    if not task.order_number >= 0:
        return ErrorCode.MINUS_NUMBER
    
    if task.deleted_at is not None:
        return ErrorCode.EDIT_DELETED_AT
    
    return 0
    
def to_category(categories):
    if isinstance(categories, (tuple, list)):
        if isinstance(categories[0], (tuple, list, dict)):
            return [to_category(i) for i in categories]
        else:
            categories = dict(zip(category_keys, categories))
    res = Category(**categories)
    return res

def to_task(tasks):
    if isinstance(tasks, (tuple, list)):
        if isinstance(tasks[0], (tuple, list, dict)):
            return [to_task(i) for i in tasks]
        else:
            tasks = dict(zip(task_keys, tasks))
    res = Task(**tasks)
    return res

def to_list(data):
    if isinstance(data, (tuple, list)):
        if isinstance(data[0], (dict, Category, Task)):
            return [to_list(i) for i in data]
    else:
        if isinstance(data, (dict, Category, Task)):
            return [i[1] for i in list(data)]

def to_dict(data):
    if isinstance(data, (tuple, list)):
        if isinstance(data[0], (tuple, list, Category, Task)):
            return [to_dict(i) for i in data]
        if len(data) == len(category_keys):
            return dict(zip(category_keys, data))
        if len(data) == len(task_keys):
            return dict(zip(task_keys, data))
    else:
        if isinstance(data, (Category, Task)):
            return dict(data)

def merge_percent(data):
    if isinstance(data, list):
        return [merge_percent(i) for i in data]
    if isinstance(data, dict):
        tasks = execute_SQL('SELECT * FROM Tasks WHERE category_id = ? AND deleted_at IS NULL', data["id"])
        if len(tasks) > 0:
            s = [i['status'] for i in to_dict(tasks)]
            status = int(s.count(TaskStatus.DONE) / len(s) * 100)
            data['status'] = status
        else:
            data['status'] = 0
        return data

def get_max_order_number_categories():
    n = execute_SQL('SELECT MAX(order_number) FROM Categories')[0][0]
    if n is None:
        return 0
    else:
        return n

def get_max_order_number_tasks(category_id):
    n = execute_SQL('SELECT MAX(order_number) FROM Tasks WHERE category_id = ?', category_id)[0][0]
    if n is None:
        return 0
    else:
        return n

app = FastAPI()

# CORSを回避するために追加（今回の肝）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.exception_handler(RequestValidationError)
async def handler(request:Request, exc:RequestValidationError):
    print(exc)
    return JSONResponse(content={}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@app.get('/')
def get_hello():
    return {'message': 'Hello from FastAPI Server!'}

@app.get('/categories/')
def get_all_categories(start: int = 0, limit: int = 20):
    return merge_percent(to_dict(execute_SQL('SELECT * FROM Categories ORDER BY order_number LIMIT ? OFFSET ?', limit, start)))

@app.post('/categories/')
def create_category(req: Category):
    if check_category(req) != 0:
        return {'message': 'error', 'error_type': check_category(req)}
    order_number = get_max_order_number_categories() + 1
    execute_SQL('INSERT INTO Categories(name, limit_date, order_number) values (?, ?, ?)', req.name, req.limit_date.strftime("%Y-%m-%d %H:%M:%S"), order_number)
    id = execute_SQL('SELECT * FROM sqlite_sequence WHERE name = "Categories"')[0][1]
    return {'message': 'create', 'id': id, 'name': req.name, 'description':req.description, 'limit_date': req.limit_date.strftime("%Y-%m-%d %H:%M:%S"), 'order_number': order_number}

@app.get('/categories/{id}')
def get_category(id: int):
    if check_id_categories(id):
        return {'message': 'error', 'error_type': ErrorCode.ID_NOT_FOUND}
    return merge_percent(to_dict(execute_SQL('SELECT * FROM Categories WHERE ID = ?', id)[0]))

@app.put('/categories/{id}')
def update_category(id: int, req: Category):
    if check_id_categories(id):
        return {'message': 'error', 'error_type': ErrorCode.ID_NOT_FOUND}
    if check_category(req) != 0:
        return {'message': 'error', 'error_type': check_category(req)}
    data = to_category(execute_SQL('SELECT * FROM Categories WHERE ID = ?', id)[0])
    if data.order_number > req.order_number:
        execute_SQL('UPDATE Categories SET order_number = order_number + 1 WHERE order_number >= ? AND order_number < ? AND deleted_at IS NULL', req.order_number, data.order_number)
    if data.order_number < req.order_number:
        execute_SQL('UPDATE Categories SET order_number = order_number - 1 WHERE order_number > ? AND order_number <= ? AND deleted_at IS NULL', data.order_number, req.order_number)
    execute_SQL('UPDATE Categories SET name = ?, description = ?, limit_date = ?, order_number = ? WHERE ID = ?', req.name, req.description, req.limit_date.strftime("%Y-%m-%d %H:%M:%S"), req.order_number, id)
    return {'message': 'update', 'id': id, 'name': req.name, 'description':req.description, 'limit_date': req.limit_date.strftime("%Y-%m-%d %H:%M:%S"), 'order_number': req.order_number}

@app.delete('/categories/{id}')
def delete_category(id: int):
    if check_id_categories(id):
        return {'message': 'error', 'error_type': ErrorCode.ID_NOT_FOUND}
    data = to_category(execute_SQL(f'SELECT * FROM Categories WHERE ID = {id}')[0])
    execute_SQL('UPDATE Categories SET deleted_at = ? WHERE ID = ?', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), id)
    execute_SQL('UPDATE Tasks SET deleted_at = ? WHERE category_id = ?', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), id)
    execute_SQL('UPDATE Categories SET order_number = order_number - 1 WHERE order_number > ? AND deleted_at IS NULL', data.order_number)
    return {'message': 'delete', 'id': id, 'name': data.name, 'description':data.description, 'limit_date': data.limit_date.strftime("%Y-%m-%d %H:%M:%S"), 'order_number': data.order_number}

@app.get('/categories/{id}/tasks/')
def get_tasks_in_category(id: int, start: int = 0, limit: int = 20):
    if check_id_categories(id):
        return {'message': 'error', 'error_type': ErrorCode.ID_NOT_FOUND}
    return to_dict(execute_SQL('SELECT * FROM Tasks WHERE category_id = ? ORDER BY order_number LIMIT ? OFFSET ?', id, limit, start))

@app.get('/tasks/')
def get_all_tasks(start: int = 0, limit: int = 20):
    return to_dict(execute_SQL('SELECT * FROM Tasks ORDER BY order_number LIMIT ? OFFSET ?', limit, start))

@app.post('/tasks/')
def create_task(req: Task):
    if check_id_categories(req.category_id):
        return {'message': 'error', 'error_type': ErrorCode.ID_NOT_FOUND}
    if check_task(req) != 0:
        return {'message': 'error', 'error_type': check_task(req)}
    order_number = get_max_order_number_tasks(req.category_id) + 1
    execute_SQL('INSERT INTO Tasks(name, category_id, description, status, order_number) values (?, ?, ?, ?, ?)', req.name, req.category_id, req.description, 0, order_number)
    id = execute_SQL('SELECT * FROM sqlite_sequence WHERE name = "Tasks"')[0][1]
    return {'message': 'create', 'id': id, 'name': req.name, 'category_id': req.category_id, 'description': req.description, 'status': req.status, 'order_number': order_number}

@app.get('/tasks/{id}')
def get_task(id: int):
    if check_id_tasks(id):
        return {'message': 'error', 'error_type': ErrorCode.ID_NOT_FOUND}
    return to_dict(execute_SQL('SELECT * FROM Tasks WHERE ID = ?', id)[0])

@app.put('/tasks/{id}')
def update_task(id: int, req: Task):
    if check_id_tasks(id):
        return {'message': 'error', 'error_type': ErrorCode.ID_NOT_FOUND}
    if check_task(req) != 0:
        return {'message': 'error', 'error_type': check_task(req)}
    data = to_task(execute_SQL('SELECT * FROM Tasks WHERE ID = ?', id)[0])
    if data.order_number > req.order_number:
        execute_SQL('UPDATE Tasks SET order_number = order_number + 1 WHERE order_number >= ? AND order_number < ? AND category_id = ? AND deleted_at IS NULL', req.order_number, data.order_number, data.category_id)
    if data.order_number < req.order_number:
        execute_SQL('UPDATE Tasks SET order_number = order_number - 1 WHERE order_number > ? AND order_number <= ? AND category_id = ? AND deleted_at IS NULL', req.order_number, data.order_number, data.category_id)
    execute_SQL('UPDATE Tasks SET name = ?, category_id = ?, description = ?, status = ?, order_number = ? WHERE ID = ?', req.name, data.category_id, req.description, req.status, req.order_number, id)
    return {'message': 'update', 'id': id, 'name': req.name, 'category_id': data.category_id, 'description': req.description, 'status': req.status, 'order_number': req.order_number}

@app.delete('/tasks/{id}')
def delete_task(id: int):
    if check_id_tasks(id):
        return {'message': 'error', 'error_type': ErrorCode.ID_NOT_FOUND}
    data = to_task(execute_SQL('SELECT * FROM Tasks WHERE ID = ?', id)[0])
    execute_SQL('UPDATE Tasks SET deleted_at = ? WHERE ID = ?', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), id)
    execute_SQL('UPDATE Tasks SET order_number = order_number - 1 WHERE order_number > ? AND category_id = ? AND deleted_at IS NULL', data.order_number, data.category_id)
    return {'message': 'delete', 'id': id, 'name': data.name, 'category_id': data.category_id, 'description': data.description, 'status': data.status, 'order_number': data.order_number}
async def root():
    return {"message": "Hello World"}
