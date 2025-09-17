from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS   

# create db object global
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # init db with app
    db.init_app(app)

    # enable CORS (important for React frontend)
    CORS(app, supports_credentials=True)

    # import blueprints
    from app.routes.auth import auth_bp
    from app.routes.task import task_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")   
    app.register_blueprint(task_bp, url_prefix="/task")

    return app
