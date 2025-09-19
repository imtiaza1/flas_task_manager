from flask import Blueprint, request, jsonify, make_response, current_app
from app.models.user import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from app.utils.required_token import token_required

auth_bp = Blueprint("auth", __name__)

# REGISTER
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "username and password required", "success": False}), 400

    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"message": "User already exists", "success": False}), 409

    hashed_pw = generate_password_hash(password)

    new_user = User(username=username, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Register successful", "success": True}), 201


# LOGIN
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "username and password required", "success": False}), 400

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        # generate JWT (1 day expiry)
        token = jwt.encode(
            {
                "user_id": user.id,
                "username": user.username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
            },
            current_app.config["JWT_SECRET_KEY"],
            algorithm="HS256",
        )

        # set cookie
        resp = make_response(
            jsonify(
                {
                    "message": "Login successful",
                    "success": True,
                    "user": {"id": user.id, "username": user.username}
                }
            )
        )
        resp.set_cookie(
            "jwt",
            token,
            httponly=True,  # JS se access na ho
            samesite="none",  # React + Flask ke liye safe
            secure=True,  # dev ke liye false; prod me True karna
            max_age=60*60*24
        )
        return resp, 200

    return jsonify({"message": "Invalid credentials", "success": False}), 401

@auth_bp.route("/check", methods=["GET"])
@token_required
def check(current_user):
    return jsonify({
        "success": True,
        "user": {"id": current_user.id, "username": current_user.username}
    }), 200

# LOGOUT
@auth_bp.route("/logout", methods=["POST"])
def logout():
    resp = make_response(jsonify({"message": "Logout success", "success": True}))
    resp.delete_cookie("jwt")
    return resp, 200
