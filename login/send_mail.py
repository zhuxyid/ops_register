#import os
#from django.core.mail import send_mail

# os.environ['DJANGO_SETTINGS_MODULE']= 'myweb.settings'
# if __name__ == '__main__':
#     send_mail(
#         '邮件主题',
#         '邮件文本内容',
#         '772931883@qq.com',   #邮件发送方,settings设置
#         ['zhuxyid@gmail.com']  #邮件接收方
#     )

import os
from django.core.mail import EmailMultiAlternatives

os.environ['DJANGO_SETTINGS_MODULE']= 'myweb.settings'
if __name__ == '__main__':
    subject, from_email, to = '来自xxx邮箱','772931883@xx.com','zhuxuy@samples.cn'
    text_content = '欢迎访问',
    html_content = '<p>xxx</p>'
    msg = EmailMultiAlternatives(subject,text_content,from_email,[to])
    msg.attach_alternative(html_content,"text/html")
    msg.send()