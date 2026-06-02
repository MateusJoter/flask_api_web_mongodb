from pydantic import BaseModel
from typing import Optional

class Categoria(BaseModel):
    id: int
    titulo: str
    subcategorias: Optional[list] = []
