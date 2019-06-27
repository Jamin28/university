from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,EqualTo,Email
from wtforms.validators import ValidationError
class PostForm(FlaskForm):
    title = StringField('标题',validators=[DataRequired(),Length(6,30,message='长度不符合要求')])
    content = TextAreaField('内容',render_kw={'placeholder':'这一刻你的想法'},validators=[DataRequired(),Length(3,300,message='长度不符合要求')])
    submit = SubmitField('发表')

