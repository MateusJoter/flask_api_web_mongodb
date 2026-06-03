from flask import Flask
from pymongo import MongoClient
from .config import Config

db = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    global db

    try:
        client = MongoClient(app.config['MONGO_URI'])
        db = client.get_default_database()
        print("Conectado ao Banco de Dados com sucesso!")

    except Exception as e:
        print(f"Erro ao se conectar ao Banco de Dados: {e}")

    from .routes.main import main_bp
    app.register_blueprint(main_bp)

    return app