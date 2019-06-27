from exts import db
from flask import current_app
from datetime import datetime
from werkzeug.security import check_password_hash,generate_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    telephone = db.Column(db.String(20),nullable=False,unique=True)
    username = db.Column(db.String(50),nullable=False)
    password_hash = db.Column(db.String(128),nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    icon = db.Column(db.String(64), default='default.jpg')

    @property
    def password(self):
        raise AttributeError('密码你不可读')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

 #生成token
    def generate_active_token(self,expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'],expires_in=expires_in)
        return s.dumps({'id':self.id})

    #检测token
    @staticmethod
    def check_active_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        u = User.query.get(data['id'])
        if not u:
            return False
        if not u.confirmed:
            u.confirmed = True
            db.session.add(u)
        return True

    def check_password(self, raw_password):
        result = check_password_hash(self.password_hash, raw_password)
        return result

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    telephone = db.Column(db.String(11),nullable=False)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Question(db.Model):
    ___tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    author = db.relationship('User',backref = db.backref('question'))

class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    movie_id = db.Column(db.Integer,db.ForeignKey('movie.id'))
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    movie = db.relationship('Movie',backref = db.backref('answers',order_by=id.desc()))
    author = db.relationship('User', backref=db.backref('answers'))

class Movie(db.Model):
    __tablename__='movie'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100),nullable=False)
    actor = db.Column(db.String(50))
    times = db.Column(db.String(50), nullable=False)
    score = db.Column(db.String(10))
    summary = db.Column(db.Text, nullable=False)