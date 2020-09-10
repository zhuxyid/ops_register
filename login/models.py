from django.db import models

# Create your models here.
class User(models.Model):
    sex = (
        ('male','男'),
        ('female','女')
    )
    username = models.CharField(max_length=128,unique=True) #用户名必须唯一的,用户名可以重复
    password = models.CharField(max_length=128) #密码后面会加密处理，这里如果设置过段可能出现密码不正确
    email = models.EmailField(unique=True)      #邮箱也是唯一
    gender = models.CharField(max_length=32,choices=sex,default="男")    #设置可选择男女,默认值男
    c_time = models.DateTimeField(auto_now_add=True)                    #自动添加创建时间
    has_confirmed = models.BooleanField(default=False)                  #新增用户是没有经过邮件确认

    def __str__(self):
        return self.username

    class Meat:
        ordering = ['-c_time']       #默认排序c_time进行排序,默认是正序列，-表示倒序，谁最后创建在最后显示
        verbose_name = '用户'
        verbose_name_plural = '用户'

class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User',on_delete=models.CASCADE)    #这里User用字符，类定义没有顺序之分。如果这里使用User,那User必须定义在上方
    c_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username + self.code
    class Meat:
        ordering = ['-c_time']
        verbose_name = '确认吗'
        verbose_name_plural = '确认吗'