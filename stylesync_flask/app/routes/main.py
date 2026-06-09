from flask import Blueprint, jsonify, request, current_app  
from pydantic import ValidationError
from app.models.user import LoginPayload, User, UserDBModel
from app import db
from bson import ObjectId # Converte a informação em id do MongoDB
from app.models.product import Product, ProductDBModel, UpdateProduct
from app.models.sale import Sale
from app.decorators import token_required
from datetime import datetime, timedelta, timezone
import jwt
import csv
import os
import io

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
@token_required
def create_product(token):
    try:
        product = Product(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()})

    result = db.products.insert_one(product.model_dump())
    return jsonify({"message": "Produto criado.",
                   "id": str(result.inserted_id)}), 201
    
# RF: O sistema deve permitir a visualização dos detalhes de um único e existente produto.
@main_bp.route('/product/<string:product_id>', methods='GET')
def get_product_by_id(product_id):
    try:
        oid = ObjectId(product_id)
    except Exception as e:
        return jsonify({'error': f'Erro ao tentar transformar {product_id} em id do Banco de Dados'}), 400

    try:
        product = db.products.find_one({'_id':oid})
        if product:
            product_model = ProductDBModel(**product).model_dump(by_alias=True, exclude_none=True)
            return jsonify(product_model)
        else:
            return jsonify({'error': f'Não foi possível encontrar produto com id {product_id}'})
    except Exception as e:
        return jsonify({'error': f'Erro ao buscar produto com id {product_id}: {e}'})

# RF: O sistema deve permitir a atualização de um único e existente produto.
@main_bp.route('/product/<string:product_id>', methods='PUT')
@token_required
def update_product(token, product_id):
    try:
        oid = ObjectId(product_id)
        update_data = UpdateProduct(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors }), 400

    update_result = db.products.update_one(
        {"_id": oid},
        {"$set": update_data.model_dump(exclude_unset=True)}
    )

    if update_result.matched_count == 0:
        return jsonify({"error": "Produto não encontrado"}), 404

    updated_product = db.products.find_one({"_id": oid})
    return jsonify(ProductDBModel(**updated_product).model_dump(by_alias=True, exclude=None))

# RF: O sistema deve permitir a deleção de um único e existente produto.
@main_bp.route('/product/<string:product_id>', methods='DELETE')
@token_required
def delete_product_by_id(token, product_id):
    try:
        oid = ObjectId(product_id)
    except Exception:
        return jsonify({"error": "id do produto não encontrado."}), 400

    delete_product = db.products.delete_one({"_id": oid})

    if delete_product.deleted_count == 0:
        return jsonify({"error": "Produto não encontrado."}), 404
    return "", 204
    
# RF: O sistema deve permitir a importação de vendas através de um arquivo.
@main_bp.route('/sales', methods='POST')
@token_required
def upload_sales(token):
    if not 'file' in request.files:
        return jsonify({"error": "Não há arquivos de entrada."}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "Não há arquivos selecionados."}), 400

    if file.filename.endswith('.csv'):
        csv_stream = io.StringIO(file.stream.read().decode('UTF-8'), newline=None)
        csv_reader = csv.DictReader(csv_stream)

        sales_to_insert = []
        errors = []

        for row_num, row in enumerate(csv_reader, 1):
            try:
                sale_data = Sale(**row)

                sales_to_insert.append(sale_data.model_dump())
            except ValidationError as e:
                errors.append(f'Linha {row_num} com dados inválidos - {e}.')
            except Exception:
                errors.append(f'Linha {row_num} com erro inesperado.')

            if sales_to_insert:
                try:
                    db.sales.insert_many(sales_to_insert)
                except Exception as e:
                    return jsonify({'error': f'{e}'})
            return jsonify({
                'message': 'Upload realizado com sucesso',
                'vendas importadas': len(sales_to_insert),
                'erros encontrados': errors
            }), 200


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

# RF: O sistema deve poder retornar uma lista de todos os usuários cadastrados sem suas senhas.
@main_bp.route('/usuarios', methods='GET')
@token_required
def get_users(token):
    users_cursor = db.users.find({})
    users_list = [UserDBModel(**user).model_dump(by_alias=True, exclude_none=True)['username'] for user in users_cursor]
    
    return jsonify(users_list), 200

# RF: O sistema deve permitir a criação de um novo usuário.
@main_bp.route('/usuarios', methods='POST')
@token_required
def create_user(token):
    try:
        raw_data = request.get_json()
        user_data = User(**raw_data)
    except ValidationError:
        return jsonify({"error": "Dados malformatados"}), 400

    result = db.users.insert_one(user_data.model_dump())
    return jsonify({"message": "Usuário criado.",
                   "id": str(result.inserted_id)}), 201

# RF: O sistema deve permitir a deleção de um usuário pelo seu id.
@main_bp.route('/usuario/<string:user_id>', methods='DELETE')
@token_required
def delete_user(token, user_id):
    try:
        oid = ObjectId(user_id)
    except Exception:
        return jsonify({"error": "Não foi possível receber o id do usuário a ser deletado"}), 400

    deleted_user = db.users.delete_one({'_id': oid})

    if deleted_user.deleted_count == 0:
        return jsonify({"error": "Usuário não encontrado"}), 404

    return "", 204


























