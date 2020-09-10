"""myweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from login import views
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.index),
    path('login/',views.login),
    path('register/',views.register),
    path('logout/', views.logout),
    path('captcha/',include('captcha.urls')),    #转发到二级路由captcha中
    path('confirm/',views.user_confirm),
]

#未登录，不论访问index还是login和logout，全部跳转到login界面，可以访问注册页面
#登陆，访问login会自动跳到index页面
#登陆，不需要访问register页面，需要先logout
#登陆后，全部跳转到login界面
