from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed,FileRequired
from wtforms import  SubmitField

from exts import photos


class UploadForm(FlaskForm):
    icon = FileField('头像', validators=[FileRequired('请选择文件'), FileAllowed(photos, message="只能选择图片")])
    submit = SubmitField('立即注册')
