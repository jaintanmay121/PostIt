"""PostIt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
# from django.views.generic.base import RedirectView
from post import views
# from django.views.generic import TemplateView
from rest_framework.documentation import include_docs_urls
# from django.conf.urls.static import static
from rest_framework.schemas import get_schema_view

API_DESCRIPTION = "Use these APIs to get details of all the posts on PostIt!."
urlpatterns = [
    url(r'^', include('post.urls')),
    path('admin/', admin.site.urls),
    # url(r'^.*$', RedirectView.as_view(url='/feed/', permanent=False), name='index'),
    url(r'^api/$', views.sendAll),
    url(r'^api/(?P<username>.*)$', views.sendUser),
    path('docs/', include_docs_urls(title='PostIt! API', description=API_DESCRIPTION), )
]
