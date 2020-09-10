from django import forms
from captcha.fields import CaptchaField

class UserForm(forms.Form):
    username = forms.CharField(label="用户",max_length=128,widget=forms.TextInput(attrs={'class':'form-contro','placeholder':'用户'}))
    password = forms.CharField(label="密码",max_length=128,widget=forms.PasswordInput(attrs={'class':'form-contro','placeholder':'密码'}))
    captcha = CaptchaField(label="验证码")

class RegisterForm(forms.Form):
    sex = (
        ('male','男'),
        ('female','女')
    )

    username = forms.CharField(label="用户", max_length=128,
                               widget=forms.TextInput(attrs={'class': 'form-contro', 'placeholder': '用户'}))
    password = forms.CharField(label="密码", max_length=128,
                               widget=forms.PasswordInput(attrs={'class': 'form-contro', 'placeholder': '密码'}))
    password_sure = forms.CharField(label="确认密码", max_length=128,
                               widget=forms.PasswordInput(attrs={'class': 'form-contro', 'placeholder': '密码'}))
    email = forms.EmailField(label="注册邮箱",widget=forms.EmailInput(attrs={'class': 'form-contro', 'placeholder': '邮箱'}))
    gender = forms.ChoiceField(label="性别",choices=sex)
    captcha = CaptchaField(label="验证码")