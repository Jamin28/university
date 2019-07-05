from captcha.fields import CaptchaField
from django.db import models
from django.core import validators
from django import forms
from django.forms import EmailField


# Create your models here.

# 电影信息



class Movie(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    length = models.CharField(max_length=50)
    release_time = models.DateField()
    score = models.FloatField()
    score_num = models.IntegerField()
    box_office = models.IntegerField()

    class Meta:
        db_table = 'movie'
        ordering = ['box_office']

# 富文本
from tinymce.models import HTMLField
class Text(models.Model):
    str = HTMLField()


# 用户
class User(models.Model):
    username = models.CharField(max_length=100,validators=[validators.MinLengthValidator(6)])
    telephone = models.CharField(max_length=11, validators=[validators.RegexValidator(r"1[3456789]\d{9}")])
    email = models.EmailField(null=False)
    password1 = models.CharField(max_length=30,validators=[validators.MinLengthValidator(6)])
    class Meta:
        db_table = 'user'


class RtimeMovie(models.Model):
    boxoffice_realtime = models.FloatField()
    boxoffice_total = models.FloatField()
    link = models.CharField(max_length=1000)
    name = models.CharField(max_length=50)
    releasetime = models.DateField()
    score = models.FloatField()
    star = models.CharField(max_length=100)

    class Meta:
        db_table = 'realtime_movie'


# 验证码captcha 的form
class CaptchaTestForm(forms.Form):
    email = EmailField(required=True,error_messages={'required':'必须填写邮箱号'},label='邮箱')
    captcha = CaptchaField()