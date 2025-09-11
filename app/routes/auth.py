from flask import Blueprint,render_template,session,redirect,url_for,render_template,request,Response,flash

auth_bp=Blueprint('auth',__name__)

USER_CREDENTIALS={
    'username':'admin',
    'password':'1234'
}

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')

        if username==USER_CREDENTIALS['username'] and password==USER_CREDENTIALS['password']==password:
            session['user']=username
            flash('login Successfull')
        else:
            flash('invalid credentials try again')
        
    return render_template('login.html')