from flask import Blueprint, request, jsonify
from app import db
from app.models.task import Task
from app.utils.required_token import token_required

task_bp = Blueprint("task", __name__)

# View all tasks
@task_bp.route("/", methods=["GET"])
@token_required
def view_task(current_user):
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return jsonify({
        "message": "Data fetch success",
        "success": True,
        "data": [task.to_dict() for task in tasks]
    }), 200


# Add a task
@task_bp.route("/add", methods=["POST"])
@token_required
def add_task(current_user):
    data = request.get_json()
    title = data.get("title")

    if not title:
        return jsonify({"message": "Title is required", "success": False}), 400

    new_task = Task(title=title, user_id=current_user.id, status="Pending")
    db.session.add(new_task)
    db.session.commit()

    return jsonify({
        "message": "Task added successfully",
        "success": True,
        "task": new_task.to_dict()
    }), 201


# Toggle task status
@task_bp.route("/toggle/<int:task_id>", methods=["PUT"])
@token_required
def toggle_task(current_user, task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({"message": "Task not found", "success": False}), 404

    data = request.get_json()
    new_status = data.get("status")

    if new_status not in ["Pending", "Working", "Done"]:
        return jsonify({"message": "Invalid status", "success": False}), 400

    task.status = new_status
    db.session.commit()

    return jsonify({
        "message": "Status updated successfully",
        "success": True,
        "task": task.to_dict()
    }), 200


# Delete a task
@task_bp.route("/delete/<int:task_id>", methods=["DELETE"])
@token_required
def delete_task(current_user, task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({"message": "Task not found", "success": False}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({
        "message": "Task deleted successfully",
        "success": True
    }), 200
