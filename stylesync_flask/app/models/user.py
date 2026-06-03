from pydantic import BaseModel
from typing import Optional 
from bson import ObjectId

''' 
Opta-se por não criar um modelo não do usuário, mas do login em si.
A ideia é utilizar a classe não para os dados do usuário, mas tão simplesmente para validar seu acesso.
'''
class LoginPayload(BaseModel):
    username: str
    password: str
    
class User(LoginPayload):
    id: Optional[ObjectId] = Field(None, alias='_id') # O alias serve para receber e enviar '_id', mas utilizar 'id' no tratamento interno

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class UserDBModel(User):
    def model_dump(self, by_alias: bool = False, exclude: Optional[set] = None):
        data = super().model_dump(by_alias=by_alias, exclude=exclude)
        if self.id:
            data['_id'] = str(data['_id'])
        return data
