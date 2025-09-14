from flask import Blueprint,render_template,session,redirect,url_for,render_template,request,Response,flash
from app.models import User
from app import db
auth_bp=Blueprint('auth',__name__)

USER_CREDENTIALS={
    'username':'admin',
    'password':'1234'
}

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # check if user exists
        user = User.query.filter_by(username=username).first()

        if user:
            flash("User already exists!", "error")
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash("User successfully added!", "success")
            return redirect(url_for('task.view_task'))  

    return render_template('register.html')

    


@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check user in database
        user = User.query.filter_by(username=username, password=password).first()

        if user:  # if user found
            session['user'] = user.username
            session['user_id']=user.id
            flash('Login Successful ✅', 'success')
            return redirect(url_for('task.view_task'))
        else:
            flash('Invalid credentials ❌', 'danger')

    return render_template('login.html')
        
@auth_bp.route('/logout')
def logout():
    session.pop('user',None)
    flash("loggout success")
    return redirect(url_for('auth.login'))