#encoding:utf-8
import os
from PIL import Image
from flask import Flask, render_template, request, redirect, url_for, session, current_app
from flask_uploads import configure_uploads, patch_request_class
import config
from forms import UploadForm
from models import User,Question,Answer,Admin,Movie
from exts import db, photos, bootstrap, mail, send_mail
from decorators import login_required

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
mail.init_app(app)
bootstrap.init_app(app)
configure_uploads(app,photos)
patch_request_class(app,size=None)
#登录性质装饰器

@app.route('/')
def index():
    context = {
        'questions':Question.query.order_by('create_time').all()
    }
    return render_template('index.html',**context)

@app.route('/moviemain/',methods=['GET','POST'])
def moviemain():
    movies = Movie.query.all()
    if request.method == 'GET':
        page = request.args.get('page',1,type=int)
        pagination = Movie.query.order_by(Movie.id).paginate(page,per_page=3,error_out=False)
        movies = pagination.items
        return render_template('moviemain.html',movies=movies,pagination=pagination)
    else:
        return render_template('moviemain.html')

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone).first()
        # 用户存在
        if user and user.check_password(password):
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('moviemain'))
        else:
            return u'手机号或密码错误，请核对后登录'

@app.route('/adminlogin/',methods=['GET','POST'])
def adminlogin():
    if request.method == 'GET':
        return render_template('adminlogin.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        admin = Admin.query.filter(Admin.telephone == telephone).first()
        if admin:
            session.permanent = True
            return redirect(url_for('adminmain'))
        else:
            return u'手机号码或者是密码错误'

@app.route('/adminmain/')
def adminmain():
    movies = Movie.query.all()
    return render_template('adminmain.html', movies=movies)

@app.route('/detail/<movie_id>/')
def detail(movie_id):
    movie_model = Movie.query.filter(Movie.id == movie_id).first()
    return render_template('detail.html',movie = movie_model)


@app.route('/register/',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        u = User(
            telephone=request.form.get('telephone'),
            username=request.form.get('username'),
            password=request.form.get('password1')
        )
        db.session.add(u)
        db.session.commit()
        token = u.generate_active_token()
        send_mail(u.telephone, "激活您的用户", 'activate', username=u.username, token=token)
        return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/activate/<token>/')
def activate(token):
    if User.check_active_token(token):
        return redirect(url_for('login'))
    else:
        return redirect(url_for('index'))

@app.route('/question/',methods=['GET','POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title,content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))

@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    admin_id = session.get('admin_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user':user}
    return {}

@app.route('/logout/')
def logout():
    session.pop('user_id')
    return redirect(url_for('login'))

@app.route('/adminlogout/')
def adminlogout():
    admin = Admin.query.filter().first()
    session['admin_id'] = admin.id
    admin_id = session.get('admin_id')
    session.pop('admin_id')
    return redirect(url_for('adminlogin'))

@app.route('/add_answer/',methods=['POST'])
@login_required
def add_answer():
    if request.method == 'POST':
        content = request.form.get('answer_content')
        movie_id = request.form.get('movie_id')
        answer = Answer(content=content)
        user_id = session['user_id']
        user = User.query.filter(User.id == user_id).first()
        answer.author = user
        movie = Movie.query.filter(Movie.id == movie_id).first()
        answer.movie = movie
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for('detail',movie_id=movie_id))
    else:
        print(request.method)

@app.route('/search/',methods=['POST'])
@login_required
def search():
    if request.method == 'POST':
        q = request.form['q']
        movies = Movie.query.filter(Movie.title.contains(q))
        return render_template('moviemain2.html',movies=movies)
    else:
        return render_template('moviemain2.html')

@app.route('/adminsearch/',methods=['POST','GET'])
def adminsearch():
    if request.method == 'POST':
        q = request.form['q']
        movies = Movie.query.filter(Movie.title.contains(q))
        return render_template('adminsearch.html',movies=movies)
    else:
        return render_template('adminsearch.html')

@app.route('/change_icon/',methods=['GET','POST'])
@login_required
def change_icon():
    form = UploadForm()

    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    if form.validate_on_submit():
        suffix = os.path.splitext(form.icon.data.filename)[1]
        filename = random_string() + suffix
        photos.save(form.icon.data,name=filename)
        pathname = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],filename)
        img = Image.open(pathname)
        img.thumbnail((128, 128))
        img.save(pathname)
        if user.icon != 'default.jpg':
            os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], user.icon))
        user.icon = filename
        db.session.add(user)
        return redirect(url_for('change_icon'))

    img_url = photos.url(user.icon)
    return render_template('change_icon.html',form=form,img_url=img_url)

def random_string(length=20):
    import random
    base_str = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.choice(base_str) for i in range(length))

@app.route('/add/',methods=['GET','POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    else:
        title = request.form.get('title')
        image = request.form.get('image')
        actor = request.form.get('actor')
        times = request.form.get('times')
        score = request.form.get('score')
        summary = request.form.get('summary')
        movie = Movie(title=title,image=image,actor=actor,times=times,score=score,summary=summary)
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for('adminmain'))

@app.route('/delete/',methods=['GET','POST'])
def delete():
    if request.method == 'GET':
        return render_template('delete.html')
    else:
        title = request.form.get('title')
        movie = Movie.query.filter_by(title= title).first()
        db.session.delete(movie)
        db.session.commit()
        return redirect(url_for('adminmain'))

@app.route('/change/',methods=['GET','POST'])
def change():
    if request.method == 'GET':
        return render_template('change.html')
    else:
        movieId = request.form.get('movieId')
        title = request.form.get('title')
        image = request.form.get('image')
        actor = request.form.get('actor')
        times = request.form.get('times')
        score = request.form.get('score')
        summary = request.form.get('summary')
        movie = Movie.query.filter_by(id=movieId).first()
        movie.title = title
        movie.image = image
        movie.actor = actor
        movie.times = times
        movie.score = score
        movie.summary = summary
        db.session.commit()
        return redirect(url_for('adminmain'))