from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from app.models.user import LoginPayload

main_bp = Blueprint('main_bp', __name__)

# RF: O sistema deve autenticar um usuário para que ele obtenha um token.
@main_bp.route('/login', methods=['POST'])
def login():
    try:
        raw_data = request.get_json()
        user_data = LoginPayload(**raw_data) # O operador ** é o que desacopla o dicionário, transformando suas keys 
                                             # em argumentos que possam ser validados pelo Loginpayload
        except ValidationError as e:
            return jsonify({"erro": e.errors()}), 400
        except Exception as e:
            return jsonify({"erro": f"Erro durante aa requisição do dado: {e}"}), 500
            
    return jsonify({"message": r"Realizar o login do usuário {user_data.model_dump_json()}."}) # model_dump_json() é a função responsável por transformar as
                                                                                               # informações da classe Loginpayload de volta para um json.

# RF: O sistema deve listar todos os produtos.
@main_bp.route('/products', methods=['GET'])
def get_products():
    return jsonify({"message": "Rota de listagem de todos os produtos."})
    
# RF: O sistema deve criar um novo produto.
@main_bp.route('/products', methods='POST')
def new_product():
    return jsonify({"message": "Rota de criação de um novo produto."})
    
# RF: O sistema deve permitir a visualização dos detalhes de um único e existente produto.
@main_bp.route('/products/<int:product_id>', methods='GET')
def get_product_by_id(product_id):
    return jsonify({"message": f"Rota de visualização do produto cujo id é {product_id}."})

# RF: O sistema deve permitir a atualização de um único e existente produto.
@main_bp.route('/products/<int:product_id>', methods='PUT')
def update_product_by_id(product_id):
    return jsonify({"message": f"Rota de atualização do produto cujo id é {product_id}."})

# RF: O sistema deve permitir a deleção de um único e existente produto.
@main_bp.route('/products/<int:product_id>', methods='DELETE')
def delete_product_by_id(product_id):
    return jsonify({"message": f"Rota de deleção do produto cujo id é {product_id}."})
    
# RF: O sistema deve permitir a importação de vendas através de um arquivo.
@main_bp.route('/sales', methods='POST')
def upload_sales():
    return jsonify({"message": "Rota de importação de vendas via arquivo."})
































