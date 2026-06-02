from pydantic import BaseModel
from typing import Optional

class Category(BaseModel):
    id: int
    title: str
    subcategories: Optional[list] = []
