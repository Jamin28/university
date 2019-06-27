from flask import Flask,Blueprint,jsonify
from app.exts import db
from flask_login import current_user

posts = Blueprint("posts",__name__)

@posts.route('/collect/<int:pid>')
def collect(pid):
    # 判断是否收藏
    if current_user.is_favorite(pid):
        current_user.del_favorite(pid)
    else:
        current_user.add_favorite(pid)
    return jsonify({'result':'ok'})