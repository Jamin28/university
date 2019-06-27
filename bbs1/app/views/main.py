from flask import Flask, Blueprint, render_template, flash, get_flashed_messages, url_for, request, current_app, \
    redirect
from flask_login import current_user

from app.exts import db
from app.forms.posts import PostForm
from app.models import Posts
from flask_paginate import Pagination,get_page_parameter

main = Blueprint("main",__name__)

@main.route('/',methods=['GET','POST'])
def index():
    form = PostForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            u = current_user._get_current_object()
            p = Posts(title=form.title.data,content=form.content.data,user=u)
            db.session.add(p)
            return redirect(url_for('main.index'))
        else:
            flash('请先登录')
            return redirect(url_for('users.login'))

    posts = Posts.query.filter_by(rid=0).all()
    # pagination = Posts.query.filter_by(rid=0).all().paginate(参数1，参数2，参数3)
    page = request.args.get('page',1,type=int)# 获取想参看第几页
    pagination = Posts.query.filter_by(rid=0).order_by(Posts.timestamp.desc()).paginate(page,per_page=3,error_out=False)
    posts = pagination.items
    return render_template('main/index.html',form=form,posts=posts,pagination=pagination)

    # page = request.args.get(get_page_parameter(),type=int, default=1)
    # start = (page - 1) * current_app.config['PERPAGE_NUM']
    # end = start + current_app.config['PERPAGE_NUM']
    # posts = Posts.query.slice(start,end)
    # pagination = Pagination(bs_version=3,page=page,total=Posts.query.count(),outer_window=0,inner_window=2)
    #
    # context = {
    #     'form':form,
    #     'posts':posts,
    #     'pagination':pagination
    # }
    #
    # return render_template('main/index.html',**context)

