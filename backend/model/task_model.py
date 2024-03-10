from datetime import datetime

from typing import Optional

from pydantic import BaseModel

class Task(BaseModel):
    id: int
    name: str
    category_id: int
    description: Optional[str] = ""
    status: int
    order_number: int
    deleted_at: Optional[datetime] = None