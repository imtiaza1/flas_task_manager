from flask import Flask,session,Response,request,Blueprint,jsonify
from app import db
from app.models import Task,User

task_bp=Blueprint('task',__name__)

@task_bp.route('/', methods=['GET'])
def view_task():
    if 'user' not in session:
        return jsonify({
            "message": "Please login to access this page",
            "success": False
        }), 401

    tasks = Task.query.filter_by(user_id=session['user_id']).all()
    return jsonify({
        "message": "Data fetch success",
        "success": True,
        "data": [task.to_dict() for task in tasks]  
    }), 200


@task_bp.route('/add', methods=['POST'])
def add_task():
    if 'user' not in session:
        return jsonify({
            "message": "Please login to continue",
            "success": False
        }), 401

    data = request.get_json()
    title = data.get('title')

    if not title:
        return jsonify({"message": "Title is required", "success": False}), 400

    new_task = Task(title=title, user_id=session['user_id'], status='Pending')
    db.session.add(new_task)
    db.session.commit()

    return jsonify({
        "message": "Task added successfully",
        "success": True,
        "task": new_task.to_dict()
    }), 201


@task_bp.route('/toggle/<int:task_id>', methods=['PUT'])
def toggle_task(task_id):
    if 'user' not in session:
        return jsonify({
            "message": "Please login to continue",
            "success": False
        }), 401

    task = Task.query.filter_by(id=task_id, user_id=session['user_id']).first()
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


@task_bp.route('/delete/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if 'user' not in session:
        return jsonify({
            "message": "Please login to continue",
            "success": False
        }), 401

    task = Task.query.filter_by(id=task_id, user_id=session['user_id']).first()
    if not task:
        return jsonify({"message": "Task not found", "success": False}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({
        "message": "Task deleted successfully",
        "success": True
    }), 200
