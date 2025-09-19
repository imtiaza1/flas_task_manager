import jwt
from flask import request, jsonify, current_app
from functools import wraps
from app.models.user import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("jwt")  # same name as set in login

        if not token:
            return jsonify({"message": "Token is missing!", "success": False}), 401

        try:
            data = jwt.decode(
                token,
                current_app.config["JWT_SECRET_KEY"],
                algorithms=["HS256"]
            )
            current_user = User.query.get(data["user_id"])
            if not current_user:
                return jsonify({"message": "User not found", "success": False}), 404

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired", "success": False}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token", "success": False}), 401

        return f(current_user, *args, **kwargs)

    return decorated
