from flask import Blueprint, jsonify

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def index():
    return jsonify({"message": "Bem-vindo à API da StyleSync!"})

@main_bp.route('/products')
def get_products():
    return jsonify({"message": "Lista de produtos da StyleSync."})

@main_bp.route('/login', methods=['POST'])
def login():
    return jsonify({"message": "Página de login da StyleSync."})