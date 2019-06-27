import os
from flask import Flask, Blueprint, render_template, flash, get_flashed_messages, url_for, request, redirect, session, \
    current_app
from app.exts import db, photos
from app.forms import RegisterForm, LoginForm, UploadForm
from app.email import send_mail
from app.models import Users
from flask_login import login_required,login_user,logout_user,current_user
from PIL import Image

users = Blueprint("users", __name__)


@users.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        u = Users(
            username=form.username.data,
            password=form.password.data,
            email=form.email.data
        )
        db.session.add(u)
        db.session.commit()

        token = u.generate_active_token()
        send_mail(u.email, "激活您的用户", 'mail/activate', username=u.username, token=token)
        flash("恭喜您,注册成功")
        return redirect(url_for('main.index'))
    return render_template('user/register.html', form=form)


@users.route('/activate/<token>/')
def activate(token):
    if Users.check_active_token(token):
        flash('该账户已经激活')
        return redirect(url_for('users.login'))
    else:
        flash('账户激活失败')
        return redirect(url_for('main.index'))


@users.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = Users.query.filter_by(username=form.username.data).first()
        if not u:
            flash("该用户名不存在")
        elif not u.confirmed:
            flash("该用户尚未激活请登录邮箱激活")
        # 验证密码
        elif u.verify_password(form.password.data):
            login_user(u, remember=form.remember.data)
            flash("登录成功")
            return redirect(request.args.get('next') or url_for("main.index"))
        else:
            flash("无效密码")
    return render_template('user/login.html', form=form)


#测试是否登录
@users.route('/test/')
@login_required
def test():
    return '您需要先登录'

@users.route('/logout/', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash('下次再来找我')

    return redirect(url_for('main.index'))


@users.route('/change_icon/', methods=['GET', 'POST'])
@login_required
def change_icon():
    form = UploadForm()
    img_url = ''
    if form.validate_on_submit():
        #获得后缀
        suffix = os.path.splitext(form.icon.data.filename)[1]

        #拼接文件名
        filename = random_string() + suffix
        #保存
        photos.save(form.icon.data,name=filename)

        # 生成缩略图
        pathname = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],filename)
        #打开文件
        img = Image.open(pathname)
        img.thumbnail((128,128))
        img.save(pathname)


        #如果用户头像不是默认，说明上传了头像
        #如果更新了，则删除原来的
        if current_user.icon != 'default.jpg':
            os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], current_user.icon))
        current_user.icon = filename
        db.session.add(current_user)
        flash("头像已经保存")
        return redirect(url_for('users.change_icon'))

    img_url = photos.url(current_user.icon)
    return render_template('user/change_icon.html', form=form, img_url=img_url)

def random_string(length=20):
    import random
    base_str = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.choice(base_str) for i in range(length))