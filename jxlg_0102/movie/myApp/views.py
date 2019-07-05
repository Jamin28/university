from captcha.models import CaptchaStore
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView

from myApp.forms import RegisterForm, LoginForm, TextForm
from myApp.models import Movie, User, RtimeMovie, CaptchaTestForm,Text
# from django.core.mail import send_mail
from myApp.serializers import MovieSerializers, Movie2Serializers
from myApp.utils import send_email


# 装饰器函数,没登录则会跳转到登录界面
def login_required(func):
    def inner(request, *args, **kwargs):
        v = request.session.get('user_id')
        if not v:
            return redirect('/login/')
        return func(request, *args, **kwargs)

    return inner


# 首页
def index(request):
    user_id = request.session.get('user_id')
    context = {}
    try:
        user = User.objects.get(pk=user_id)
        context['front_user'] = user
    except:
        pass
    return render(request, 'index.html')


# 用户注册
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        rform = RegisterForm(request.POST)
        if rform.is_valid():
            # print('*' * 100)
            username = rform.cleaned_data.get('username')
            password1 = rform.cleaned_data.get('password1')
            telephone = rform.cleaned_data.get('telephone')
            email = rform.cleaned_data.get('email')
            if not User.objects.filter(Q(username=username) | Q(telephone=telephone)).exists():
                # 注册到数据库中
                password1 = make_password(password1)
                user = User.objects.create(username=username, password1=password1, telephone=telephone, email=email)
                if user:
                    return redirect(reverse('myApp:index'))
            else:
                return render(request, 'register.html', context={'msg': '用户名或者手机号码已经存在'})
        return render(request, 'register.html', context={'msg': '注册失败，重新填写,请检查格式是否正确'})


# 登录
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        lform = LoginForm(request.POST)
        if lform.is_valid():
            username = lform.cleaned_data.get('username')
            password1 = lform.cleaned_data.get('password1')
            user = User.objects.filter(username=username).first()
            hash_pwd = user.password1
            # print(hash_pwd)
            # 解密后核对完成
            flag = check_password(password1, hash_pwd)

            if flag:

                request.session['user_id'] = user.id
                return redirect(reverse('myApp:index'))
            else:
                messages.info(request, '用户名或者密码错误')
                return redirect(reverse('myApp:login'))
        else:
            errors = lform.get_errors()
            for error in errors:
                messages.info(request, error)
            return render(request, 'login.html')


def logout(request):
    request.session.flush()
    return redirect(reverse('myApp:index'))


# 排行榜模块
@login_required
def mokuai(request):
    boxs = Movie.objects.order_by('-box_office')
    scores = Movie.objects.order_by('-score')
    score_nums = Movie.objects.order_by('-score_num')

    rboxs = RtimeMovie.objects.order_by('-boxoffice_realtime')
    tboxs = RtimeMovie.objects.order_by('-boxoffice_total')
    score_s = RtimeMovie.objects.order_by('-score')
    return render(request, 'mokuai.html',
                  {'boxs': boxs, 'scores': scores, 'score_nums': score_nums, 'rboxs': rboxs, 'tboxs': tboxs,
                   'score_s': score_s})


# 分页显示票房排名
def box_office(request, page_id):
    boxs = Movie.objects.order_by('-box_office')
    paginator = Paginator(boxs, 12)

    page = paginator.page(page_id)

    return render(request, 'box_office.html', {'boxs': page})


# 评论留言
@login_required
def edit(request):
    if request.method == 'GET':
        return render(request, 'edit.html')
    else:
        tform = TextForm(request.POST)
        if tform.is_valid():
            str = tform.cleaned_data.get('str')
            # print(str)
            tform.save()
        return render(request,'edit.html',context={'str':str})



# 管理员
def admin(request):
    return redirect('/admin/')


# 忘记密码
def forgetpwd(request):
    if request.method == 'GET':
        form = CaptchaTestForm()
        return render(request, 'forgetpwd.html', context={'form': form})
    else:
        # 获取提交的邮箱，发送邮件，然后通过发送的邮箱连接，设置新的密码
        email = request.POST.get('email')
        # 给此地址发送邮件
        result = send_email(email, request)
        # result 为布尔值
        return redirect(reverse('myApp:update_pwd'))


# 更新密码的view
def update_pwd(request):
    if request.method == 'GET':
        c = request.GET.get('c')
        return render(request, 'update_pwd.html', context={'c': c})
    else:
        code = request.POST.get('code')
        user_id = request.session.get(code)
        print(user_id)
        user = User.objects.get(pk=user_id)
        # 获取密码
        pwd = request.POST.get('password')
        repwd = request.POST.get('repassword')
        if pwd == repwd and user:
            pwd = make_password(pwd)
            user.password1 = pwd
            user.save()
            return render(request, 'update_pwd.html', context={'msg': '用户密码更新成功'})
        else:
            return render(request, 'update_pwd.html', context={'msg': '密码不一致'})


# 验证验证码是否匹配
def valide_code(request):
    if request.is_ajax():
        key = request.GET.get('key')
        code = request.GET.get('code')
        captcha = CaptchaStore.objects.filter(hashkey=key).first()
        if captcha.response == code.lower():
            # 正确时
            data = {'status': 1}
        else:
            # 错误的
            data = {'status': 0}
        return JsonResponse(data)

# dfw
class MovieViewSet(ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializers

class Movie2ViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = Movie2Serializers

# def test(request):
#     return redirect(reverse('myApp:test'))