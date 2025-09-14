from . import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id') ,nullable=False )
    title = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default='Pending') 

class User(db.Model):  
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False) 
