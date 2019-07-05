from django.urls import path, re_path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'mv',views.Movie2ViewSet)

app_name = 'myApp'
urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^box_office/(\d+)/$', views.box_office, name='box_office'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('mokuai/', views.mokuai, name='mokuai'),
    path('admin/',views.admin,name='admin'),
    path('forgetpwd/',views.forgetpwd,name='forgetpwd'),
    path('valide_code/',views.valide_code,name='valide_code'),
    path('update_pwd/',views.update_pwd,name='update_pwd'),
    path('movies/',views.MovieViewSet.as_view(),name='movie'),
    # path('mv/',views.test,name='test'),
]
