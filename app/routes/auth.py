from flask import Blueprint,render_template,session,redirect,url_for,render_template,request,Response,flash

auth_bp=Blueprint('auth',__name__)

USER_CREDENTIALS={
    'username':'admin',
    'password':'1234'
}

@auth_bp.route('/register',methods=['POST'])
def register():
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')

        if username==USER_CREDENTIALS['username'] and password==USER_CREDENTIALS['password']==password:
            session['user']=username
            flash('login Successfull')
            return redirect(url_for('task.view_task'))
        else:
            flash('invalid credentials try again')
        
    return render_template('login.html')
@auth_bp.route('/logout')
def logout():
    session.pop('user',None)
    flash("loggout success")
    return redirect(url_for('auth.login'))