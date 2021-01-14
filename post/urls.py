from django.urls import path#, include
from . import views
from django.conf.urls import re_path
# from django.conf.urls import url

app_name = 'post'


urlpatterns = [
    path("register/", views.register, name="register"),
    path("", views.userLogin, name="login"),
    # path("login/", views.userLogin, name="login"),
    path("feed/", views.index, name="feed"),
    path("logout", views.userLogout, name="logout"),
    path("upload/", views.index, name="upload"),
    re_path(r'^delete/(?P<pk>[0-9]+)/$', views.deletePost, name='deletePost'),
    re_path(r'^Like/(?P<pk>[0-9]+)/$', views.Like, name='Like'),
    # url(r'^api', include(router.urls)),
    ]
