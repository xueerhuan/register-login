from django.shortcuts import render,redirect
from blogapp.models import *
from django.views.decorators.csrf import csrf_exempt
import json
from blogapp.forms import *

import datetime
from django.shortcuts import render,redirect,HttpResponse
from io import BytesIO
from blogapp.models import *

# from utils import pagination
# from utils import check_code
# Create your views here.

def check_login(func):
    def inner(request, *args, **kwargs):
        if request.session.get('user_info'):
            return func(request, *args, **kwargs)
        else:
            return redirect('/login.html')
    return inner

def login(request):
    if request.method == 'GET':
        print(request.session.get('user_info'))
        if request.session.get('user_info'):
            return render(request, 'index.html')
        else:
            obj = loginForm()
            return render(request, 'login.html', {'form': obj})

    elif request.method == 'POST':
        obj = loginForm(request.POST)
        errors = {}
        if obj.is_valid():
            post_check_code = request.POST.get('check_code')
            session_check_code = request.session['check_code']
            if post_check_code.lower() == session_check_code.lower() :

                username = obj.cleaned_data.get('username')
                print(username)
                password = obj.cleaned_data.get('pwd')
                print(password)
                user_info = userInfo.objects. \
                    filter(username=username, password=password). \
                    values('uid', 'nickname',
                           'username', 'email',
                           'avatar',
                           'blog__bid',
                           'blog__site').first()

                print(user_info)
                request.session['user_info'] = user_info
                if request.POST.get('auto_login'):
                    request.session.set_expiry(60 * 60 * 24 *30)
                return render(request,'index.html')
            else:
                print(obj.errors)
                errors['check_code'] = '请输入正确的验证码！'
                return render(request, 'login.html', {'form': obj,'errors':errors})
        else:
            print(obj.errors)
            return render(request, 'login.html', {'form': obj, 'errors': errors})

def logout(request):
    request.session.clear()
    return redirect('/')

def register(request):
    if request.method == 'GET':
        obj = RegisterForm()
        return render(request,'register.html',{'form':obj})
    elif request.method == 'POST':
        obj = RegisterForm(request.POST)
        print('hell')
        # post_check_code =  request.POST.get('username')
        # session_check_code = request.session['username']
        # print(post_check_code,session_check_code)
        if obj.is_valid():
            # if post_check_code ==  session_check_code:
            # values = obj.clean()
            data = obj.cleaned_data
            print(data)
            # models.User.objects.create(
            username= data.get('username')
            password= data.get('pwd')
            email= data.get('email')
            nickname = data.get('nickname')
            # )
            userInfo.objects.create(username=username,nickname =nickname,password =password,email = email )
            request.session['is_login'] = 'true'
            request.session['user'] = data.get('username')
            return render(request, 'index.html', {'form': obj})
            # return redirect('/')
        else:
            errors = obj.errors
            print(errors)
            print('hello')

    return render(request,'register.html',{'form':obj})



# 将check_code包放在合适的位置，导入即可，我是放在utils下面
from blogapp.utils import check_code
def create_code_img(request):
    f = BytesIO() # 直接在内存开辟一点空间存放临时生成的图片
    img, code = check_code.create_validate_code() # 调用check_code生成照片和验证码
    request.session['check_code'] = code # 将验证码存在服务器的session中，用于校验
    img.save(f,'PNG') #生成的图片放置于开辟的内存中
    return HttpResponse(f.getvalue())  #将内存的数据读取出来，并以HttpResponse返回

@check_login
def index(request):
    return render(request, 'index.html')

