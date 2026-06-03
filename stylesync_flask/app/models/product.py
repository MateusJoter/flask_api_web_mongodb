from pydantic import BaseModel, Field, ConfigDict
from typing import Optional # Nos dá a possibilidade de dizer se tal atributo é opcional
from bson import ObjectId

class Products(BaseModel):
    id: Optional[Objectid] = Field(None, alias='_id') # O alias serve para receber e enviar '_id', mas utilizar 'id' no tratamento interno
    name: str
    price: float
    description: Optional[str] = None
    stock: int
    sku: str # Stock Keeping Unit

    model_config = ConfigDict(
        populate_by_name=True, # Permite que o modelo seja populado utilizando o alias='_id'
        arbitrary_types_allowed=True # Permite utilizar o ObjectId no Optional
    )

class ProductDBModel(Products):
    def model_dump(self, by_alias: bool = False, exclude: Optional[set] = None):
        data = super().model_dump(by_alias=by_alias, exclude=exclude)
        if self.id:
            data['_id'] = str(data['_id'])
        return data

class UpdateProducts(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    stock: Optional[int] = None
