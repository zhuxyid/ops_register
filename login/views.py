from django.shortcuts import render,redirect,HttpResponse
from . import models
from . import forms
from django.conf import settings
# Create your views here.
import hashlib
import datetime

def hash_code(s,salt="myweb"):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") #生成当前字符串

    code = hash_code(user.username,now)
    print(user.username, now, code)
    models.ConfirmString.objects.create(code=code,user=user)
    return code

def send_email(email,code):
    from django.core.mail import EmailMultiAlternatives
    subject = '来自ops.zhuxyid.com注册邮件确认'
    text_content =  '''
                    这是一封来自ops.zhuxyid.com网站的地址,专注运维开发等分享内容
                    '''
    html_content =  '''
                    <p>感谢注册，点击 <a href='http://{}/confirm/?code={}'>ops.zhuxyid.com </a>进行邮件确认,有效期{}天</p>
                    '''.format('127.0.0.1:8000',code,settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject,text_content,settings.EMAIL_HOST_USER,[email])
    msg.attach_alternative(html_content,"text/html")
    msg.send()


def index(request):
    if not request.session.get('is_login',None):
        return redirect("/login/")
    return render(request, "index.html")

def login(request):
    if request.session.get('is_login',None):    #如果用户已经登陆让他跳到index页面，不允许重复登陆
        return redirect('/index/')
    if request.method == "POST":
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        # message = "请检查填写内容"
        # if username and password:
        #     try:
        #         user = models.User.objects.get(username=username)
        #     except:
        #         message = "用户或密码错误"
        #         return render(request, "login.html",locals())
        #     if user.password == password:
        #         print(username,password)
        #         return redirect('/index/')
        login_form = forms.UserForm(request.POST)
        message = "请检查填写内容"
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            print(username,password)
            try:
                user = models.User.objects.get(username=username)
            except:
                message = "用户不存在"
                return render(request, "login.html",locals())
            if user.password != hash_code(password):
                message = "用户名密码错误"
                return render(request, 'login.html', locals())
            if not user.has_confirmed:
                message = '该用户未通过邮件确认'
                return render(request,'login.html',locals())


            if user.password == hash_code(password):        #在数据库中取到password指对比用户输入密码加密后的指
                request.session['is_login'] = True
                request.session['username'] = username
                return redirect('/index/')

        else:
            return render(request, "login.html",locals())
    login_form = forms.UserForm()
    return render(request, "login.html",locals())



def register(request):
    if request.session.get('is_login',None):
        return redirect('/index')
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写内容"
        if register_form.is_valid():        #这里会自动验证验证码,下面不需要获得掩码
            username = register_form.cleaned_data.get('username')
            password = register_form.cleaned_data.get('password')
            password_sure = register_form.cleaned_data.get('password_sure')
            email = register_form.cleaned_data.get('email')
            gender = register_form.cleaned_data.get('gender')
            if password != password_sure:
                message = "密码不相同"
                return render(request,'register.html',locals())
            else:
                same_name_user = models.User.objects.filter(username=username)
                same_email_user = models.User.objects.filter(email=email)
                if same_name_user:
                    message = "用户名已存在"
                    return render(request,'register.html',locals())
                if same_email_user:
                    message = "邮箱已被注册"
                    return render(request,'register.html',locals())

                new_user = models.User()
                new_user.username=username
                new_user.password=hash_code(password)
                new_user.email=email
                new_user.gender=gender
                new_user.save()
                code = make_confirm_string(new_user)
                print(code)
                try:
                    send_email(email,code)

                except:
                    message = "邮箱发送失败"
                    return render(request, "register.html", locals())
                message = "请前往邮箱{}进行验证".format(email)
                return render(request, "register.html", locals())



        else:
            return render(request, 'register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, "register.html",locals())




def logout(request):
    if not request.session.get('is_login',None):
        return redirect('/login/')
    request.session.flush()
    return redirect("/login/")



def user_confirm(request):
    code = request.GET.get('code',None)
    message = ""
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = "无效确认请求"
        return render(request,'confirm.html',locals())
    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = "邮件过期，重新注册！"
        return render(request,'confirm.html',locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = "感谢{}确认请登陆!".format(confirm.user)
        return render(request,'confirm.html',locals())