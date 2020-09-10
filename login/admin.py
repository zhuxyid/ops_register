from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.User)    #注册User到后台
# 这里的User不要跟下面搞混
# from django.contrib.auth.models import User
admin.site.register(models.ConfirmString)