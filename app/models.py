from db import db

class Task(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    status=db.column(db.String(20),default='pending')