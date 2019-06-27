from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,EqualTo,Email
from wtforms.validators import ValidationError
from flask_wtf.file import FileField,FileAllowed,FileRequired
from app.exts import photos
#用户注册表单
from app.models import Users


class RegisterForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired(),Length(6,20,message="用户名必须在6-20之间")])
    email = StringField('Email',validators=[Email(message="请写正确的邮箱")])
    password = PasswordField('密码',validators=[DataRequired(),Length(6,20,message="密码长度必须在6-20之间")])
    confirm = PasswordField('确认密码',validators=[EqualTo('password',message="两次密码不一致")])
    submit = SubmitField('立即注册')

    #自定义验证函数
    def validata_username(self,filed):
        if Users.query.filter_by(username=filed.data).first():
            raise ValidationError("该用户已经注册，请更改")

    def validata_email(self, filed):
        if Users.query.filter_by(email=filed.data).first():
            raise ValidationError("该邮箱已经注册，请更改")

#登录表单
class LoginForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired(),Length(6,20,message="用户名必须在6-20之间")])
    password = PasswordField('密码',validators=[DataRequired(),Length(6,20,message="密码长度必须在6-20之间")])
    remember = BooleanField('记住我')
    submit = SubmitField('立即登录')
#头像上传表单
class UploadForm(FlaskForm):
    icon = FileField('头像',validators=[FileRequired('请选择文件'),FileAllowed(photos,message="只能选择图片")])
    submit = SubmitField('立即注册')