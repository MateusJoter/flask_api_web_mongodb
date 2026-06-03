from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from app.models.user import LoginPayload
from app import db
from bson import ObjectId # Converte a informação em id do MongoDB
from app.models.products import *
from app.decorators import token_required
from datetime import datetime, timedelta, timezone
import jwt

main_bp = Blueprint('main_bp', __name__)

# RF: O sistema deve autenticar um usuário para que ele obtenha um token.
@main_bp.route('/login', methods=['POST'])
def login():
    try:
        raw_data = request.get_json()
        user_data = LoginPayload(**raw_data) # O operador ** é o que desacopla o dicionário, transformando suas keys 
                                             # em argumentos que possam ser validados pelo LoginPayload
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    except Exception as e:
        return jsonify({"errors": f"Erro durante a requisição do dado: {e}"}), 500

    if user_data.username == 'admin' and user_data.password == 'supersecret':
        token = jwt.encode(
            {
                'user_id': user_data.username,
                'exp': datetime.now(timezone.utc) + timedelta(minutes=30)
            },
            current_app.config('SECRET_KEY'),
            algorithm='HS256'
        )

        return jsonify({'access_token': token}), 200
        
    return jsonify({"error": "Credenciais inválidas."}), 401

# RF: O sistema deve listar todos os produtos.
@main_bp.route('/products', methods=['GET'])
def get_products():
    products_cursor = db.products.find({})
    products_list = [ProductDBModel(**product).model_dump(by_alias=True, exclude_none=True) for product in products_cursor]
        
    return jsonify(products_list)
    
# RF: O sistema deve criar um novo produto.
@main_bp.route('/products', methods='POST')
def create_product():
    return jsonify({"message": "Rota de criação de um novo produto."})
    
# RF: O sistema deve permitir a visualização dos detalhes de um único e existente produto.
@main_bp.route('/product/<string:product_id>', methods='GET')
def get_product_by_id(product_id):
    try:
        oid = ObjectId(product_id)
    except Exception as e:
        return jsonify('error': f'Erro ao tentar transformar {product_id} em id do Banco de Dados')
    
    try:
        product = db.products.find_one({'_id':oid})
        if product:
            product_model = ProductDBModel(**product).model_dump(by_alias=True, exclude_none=True)
            return jsonify(product_model)
        else jsonify('error': f'Não foi possível encontrar produto com id {product_id}')
    except Exception as e:
        return jsonify('error': f'Erro ao buscar produto com id {product_id}: {e}')

# RF: O sistema deve permitir a atualização de um único e existente produto.
@main_bp.route('/product/<int:product_id>', methods='PUT')
def update_product_by_id(product_id):
    return jsonify({"message": f"Rota de atualização do produto cujo id é {product_id}."})

# RF: O sistema deve permitir a deleção de um único e existente produto.
@main_bp.route('/product/<int:product_id>', methods='DELETE')
def delete_product_by_id(product_id):
    return jsonify({"message": f"Rota de deleção do produto cujo id é {product_id}."})
    
# RF: O sistema deve permitir a importação de vendas através de um arquivo.
@main_bp.route('/sales', methods='POST')
def upload_sales():
    return jsonify({"message": "Rota de importação de vendas via arquivo."})

# RF: O sistema deve criar uma categoria.
@main_bp.route('/categories', methods='POST')
def create_category():
    return jsonify({"message": "Rota de criação de uma nova categoria."})

# RF: O sistema deve exibir todas as categorias disponíveis em ordem alfabética.
@main_bp.route('/categories', methods='GET')
def get_categories():
    # Ordenar categorias
    return jsonify({"message": "Rota de exibição de todas as categorias."})

# RF: O sistema deve exibir todas asubcategorias disponíveis ds e uma categoria.
@main_bp.route('/categories/<int:category_id>', methods='GET')
def get_subcategories_by_id(category_id):
    return jsonify({"message": f"Rota de exibição de todas as subcategorias da categoria cujo id é {category_id}."})

# RF: O sistema deve permitir a edição de uma única e existente categoria.
@main_bp.route('/categories/<int:category_id>', methods='PUT')
def update_category_by_id(category_id):
    return jsonify({"message": f"Rota de edição da categoria cujo id é {category_id}."})




























