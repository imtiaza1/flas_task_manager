import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv  

# Load env file
load_dotenv()

# create db object global
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # Configs (env se load karna best hai)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "secret_key")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///todo.db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # JWT secret
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "supersecretjwt")

    # Init extensions
    db.init_app(app)
    jwt.init_app(app)

    # Enable CORS for frontend
    CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

    # Import blueprints
    from app.routes.auth import auth_bp
    from app.routes.task import task_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")   
    app.register_blueprint(task_bp, url_prefix="/task")

    return app
