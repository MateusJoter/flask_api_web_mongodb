from pydantic impor BaseModel

''' 
Opta-se por não criar um modelo não do usuário, mas do login em si.
A ideia é utilizar a classe não para os dados do usuário, mas tão simplesmente para validar seu acesso.
'''
class LoginPayload(baseModel):
    username: str
    password: str
