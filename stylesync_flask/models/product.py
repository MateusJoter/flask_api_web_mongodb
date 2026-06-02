from pydantic import BaseModel
from typing import Optional # Nos dá a possibilidade de dizer se tal atributo é opcional

class Products(BaseModel):
    id: int
    name: str
    price: float
    description: Optional[str] = None
    stock: int
    sku: str # Stock Keeping Unit
