#导入类库
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_moment import Moment
from flask_migrate import Migrate
from flask_uploads import UploadSet,IMAGES,configure_uploads,patch_request_class
from flask_login import LoginManager
#创建对象
loginmanager = LoginManager()
bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
migrate = Migrate(db=db)
moment = Moment()
photos = UploadSet('photos',IMAGES)


#将扩展库对象跟 我们app进行绑定
def config_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app)
    moment.init_app(app)

    configure_uploads(app,photos)
    patch_request_class(app,size=None)
    loginmanager.init_app(app)

    #设置登录站点
    loginmanager.login_view='users.login'

    #设定登录信息
    loginmanager.login_message='请先登录'

    #保护级别
    loginmanager.session_protection = 'strong'
