from typing import Any, List, Dict, Union

from app.backend.model.category_model import Category

from app.backend.model.task_model import Task

class Converter:
    CATEGORY_KEYS = ('id', 'name', 'description', 'limit_date', 'order_number', 'deleted_at')

    TASK_KEYS = ('id', 'name', 'category_id', 'description', 'status', 'order_number', 'deleted_at')

    @staticmethod
    def to_category(categories: Union[List[Any], Dict[Any], Task]) -> Category:
        if isinstance(categories, (tuple, list)):
            if isinstance(categories[0], (tuple, list, dict)):
                return [Converter.to_category(i) for i in categories]
            else:
                categories = dict(zip(Converter.CATEGORY_KEYS, categories))
        res = Category(**categories)
        return res
    
    @staticmethod
    def to_task(tasks: Union[List[Any], Dict[Any], Category]) -> Task:
        if isinstance(tasks, (tuple, list)):
            if isinstance(tasks[0], (tuple, list, dict)):
                return [Converter.to_task(i) for i in tasks]
            else:
                tasks = dict(zip(Converter.TASK_KEYS, tasks))
        res = Task(**tasks)
        return res
    
    @staticmethod
    def to_list(data: Union[Dict[Any], Category, Task]) -> List[Any]:
        if isinstance(data, (tuple, list)):
            if isinstance(data[0], (dict, Category, Task)):
                return [Converter.to_list(i) for i in data]
        else:
            if isinstance(data, (dict, Category, Task)):
                return [i[1] for i in list(data)]
    
    @staticmethod
    def to_dict(data: Union[List[Any], Category, Task]) -> Dict[Any]:
        if isinstance(data, (tuple, list)):
            if isinstance(data[0], (tuple, list, Category, Task)):
                return [Converter.to_dict(i) for i in data]
            if len(data) == len(Converter.CATEGORY_KEYS):
                return dict(zip(Converter.CATEGORY_KEYS, data))
            if len(data) == len(Converter.TASK_KEYS):
                return dict(zip(Converter.TASK_KEYS, data))
        else:
            if isinstance(data, (Category, Task)):
                return dict(data)