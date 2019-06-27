from app.exts import db
from .users import Users
from .posts import Posts


#添加用户与帖子收藏的中间表
collections = db.Table("collections",
    db.Column('users_id',db.Integer,db.ForeignKey('users.id')),
    db.Column('posts_id',db.Integer,db.ForeignKey('posts.id'))

)