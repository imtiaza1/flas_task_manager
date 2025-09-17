from flask import Blueprint, request, jsonify, session
from app.models import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

# REGISTER
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "username and password required", "success": False}), 400

    # check if user exists
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"message": "User already exists", "success": False}), 409

    # hash password before saving
    hashed_pw = generate_password_hash(password)

    new_user = User(username=username, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "Register successful",
        "success": True,
        "user": {"id": new_user.id, "username": new_user.username}
    }), 201


# LOGIN
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "username and password required", "success": False}), 400

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        # flask session (for now)
        session["user"] = user.username
        session["user_id"] = user.id

        return jsonify({
            "message": "Login successful",
            "success": True,
            "user": {"id": user.id, "username": user.username}
        }), 200
    else:
        return jsonify({"message": "Invalid credentials", "success": False}), 401
    
@auth_bp.route("/check",methods=['GET'])
def check_login():
    if "user" in session:
        return jsonify({"success": True, "user": session["user"]}), 200
    return jsonify({"success": False}), 401


# LOGOUT
@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
    return jsonify({"message": "Logout success", "success": True}), 200
