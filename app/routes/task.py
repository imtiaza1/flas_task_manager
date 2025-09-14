from flask import Flask,redirect,session,Response,url_for,render_template,flash,request,Blueprint
from app import db
from app.models import Task,User

task_bp=Blueprint('task',__name__)

@task_bp.route('/')
def  view_task():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    task=Task.query.filter_by(user_id=session['user_id']).all()
    return render_template('task.html',tasks=task)

@task_bp.route('/add',methods=['POST'])
def add():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    title=request.form.get('title')
    if title:
        new_task=Task(title=title,user_id=session['user_id'], status='pending')
        db.session.add(new_task)
        db.session.commit()
        flash("task added successfully",'success')
    return redirect(url_for('task.view_task'))

@task_bp.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    task = Task.query.get(task_id)
    if task:
        new_status = request.form.get('status')  
        if new_status in ["Pending", "Working", "Done"]:
            task.status = new_status
            db.session.commit()
    return redirect(url_for('task.view_task'))


@task_bp.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('task.view_task'))

        


