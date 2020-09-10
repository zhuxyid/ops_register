# 可重用系统

>settings需要设置以下配置

```shell script
SECRET_KEY
EMAIL_HOST_USER
EMAIL_HOST_PASSWORD
```

>环境安装
```shell script
pip -r install requrements.txt
```

>路由说明
```shell script
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.index),
    path('login/',views.login),
    path('register/',views.register),
    path('logout/', views.logout),
    path('captcha/',include('captcha.urls')), #图形验证码
    path('confirm/',views.user_confirm),      #邮箱验证
]
#路由功能说明
当未登陆用户访问/index,/logout会自动跳转/login
当已登陆用户访问/register,会自动跳到/index
用户注册完毕后，需要通过邮件验证，否则登陆不了系统
```