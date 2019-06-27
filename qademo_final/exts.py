from flask import current_app, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from threading import Thread

from flask_uploads import UploadSet, IMAGES

photos = UploadSet('photos',IMAGES)
db = SQLAlchemy()
mail = Mail()
bootstrap = Bootstrap()


#封装函数 发送邮件
def send_mail(to,subject,template,**kwargs):
    #根据current_app 获取当前app的实例 跨页面调用  我们需要用current_app
    app = current_app._get_current_object()
    msg = Message(subject=subject,recipients=[to],sender=app.config['MAIL_USERNAME'])
    print(app.config['MAIL_USERNAME'])
    msg.html = render_template(template+'.html',**kwargs)
    msg.body = render_template(template+'.txt',**kwargs)
    #创建线程
    thr = Thread(target=async_send_mail,args=[app,msg])
    thr.start()

    return thr
def async_send_mail(app,msg):
    with app.app_context():
        mail.send(message=msg)