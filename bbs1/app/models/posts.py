from app.exts import db
from datetime import datetime

class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    rid = db.Column(db.Integer,index=True,default=0)  # 回复
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.TEXT,nullable=False)
    timestamp = db.Column(db.DateTime,default=datetime.now,nullable=False)

    uid = db.Column(db.Integer,db.ForeignKey('users.id'))

