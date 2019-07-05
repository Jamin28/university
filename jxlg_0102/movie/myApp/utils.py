# 发送邮件
import uuid

from django.core.mail import send_mail

from movie.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
from myApp.models import User


def send_email(email, request):
    subject = '找回密码'
    user = User.objects.filter(email=email).first()
    ran_code = uuid.uuid4()
    print(ran_code)
    print(type(ran_code))
    ran_code = str(ran_code)
    print(type(ran_code))
    ran_code = ran_code.replace('-', '')
    request.session[ran_code] = user.id
    message = '''
               可爱的用户：
                   您好！此链接用于找回密码，请点击链接:<a href='http://127.0.0.1:8000/update_pwd/?c=%s'>更新密码</a>
               如果链接不能点击，请复制:  
               http://127.0.0.1:8000/update_pwd/?c=%s

               来自XXX
        ''' % (ran_code, ran_code)

    result = send_mail(subject,"",  EMAIL_HOST_USER, [email, ], html_message=message, auth_password=EMAIL_HOST_PASSWORD)
    return result
