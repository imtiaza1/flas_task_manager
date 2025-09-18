from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS   
from datetime import timedelta

# create db object global
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret_key'
    app.config.update(
    SESSION_COOKIE_SAMESITE="none",
    SESSION_COOKIE_SECURE=False,  # local testing ke liye False (production me True rakhna)
    SESSION_COOKIE_HTTPONLY=True
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)
    
    # init db with app
    db.init_app(app)

    # enable CORS (important for React frontend)
    CORS(app, supports_credentials=True,origins=["http://localhost:5173"])

    # import blueprints
    from app.routes.auth import auth_bp
    from app.routes.task import task_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")   
    app.register_blueprint(task_bp, url_prefix="/task")

    return app
