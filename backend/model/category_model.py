from datetime import datetime

from typing import Optional

from pydantic import BaseModel

class Category(BaseModel):
    id: int
    name: str
    description: Optional[str] = ""
    limit_date: datetime
    order_number: int
    deleted_at: Optional[datetime] = None