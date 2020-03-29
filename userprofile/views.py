from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from .forms import UserLoginForm, UserRegisterForm
from .models import Profile
from .forms import ProfileForm

def user_login(request):
    #post请求提交表单
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        #如果数据符合表单模型要求
        if user_login_form.is_valid():
            #.cleaned_data,清洗出合法数据
            print(user_login_form)
            data = user_login_form.cleaned_data
            print(data)
            #检验账号密码是否正确匹配数据库的某个用户
            #如果均匹配成功则返回这个user对象
            user = authenticate(username=data['username'], password=data['password'])
            #如果匹配成功则user不为空
            if user:
                #将用户数据保存在session中,就实现了登录操作
                login(request,user)
                return redirect("article:article_list")
            else:
                return HttpResponse("账号或密码输入有误,请重新输入~")
        else:
            return HttpResponse("账号或密码输入不合法")
    #get请求获取表单
    elif request.method == 'GET':
        #创建表单对象
        user_login_form = UserLoginForm()
        #用于返回的变量
        context = {'form':  user_login_form}
        #返回页面和变量
        return render(request,'userprofile/login.html',context)
    #既不是post也不是get请求
    else:
        return HttpResponse("请使用GET或POST请求数据")

#用户注册
def user_register(request):
    #post请求提交表单
    if request.method == 'POST':
        #创建用户注册表单实例并赋值
        user_register_form = UserRegisterForm(data = request.POST)
        if user_register_form.is_valid():
            #保存用户注册表单实例，暂时不提交到数据库
            new_user = user_register_form.save(commit=False)
            #设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            #设置密码后的表单对象存入数据库
            new_user.save()
            #保存好数据库后立刻登录并返回博客列表页面
            login(request,new_user)
            return redirect("article:article_list")
        else:
            return HttpResponse("注册表单输入有误，请重新输入。")
    elif request.method == 'GET':
        #创建空注册表单实例
        user_register_form = UserRegisterForm()
        #返回的数据
        context = {'form' : user_register_form}

        return render(request,'userprofile/register.html',context)
    else:
        return HttpResponse("请使用GET或POST请求")

#用户退出
def user_logout(request):
    #使用logout类中的方法退出登录
    logout(request)
    #返回文章列表页面
    return redirect("article:article_list")

#用户注销账号
#python装饰器
#要掉用delete函数必须要登录,没有登录则重定向到登录页面
@login_required(login_url='/userprofile/login/')
def user_delete(request,id):
    #判断请求方式
    if request.method == "POST":
        #根据id获取需要操作的对象
        user = User.objects.get(id=id)
        #验证登录用户，和需要执行删除操作的用户是否相同
        if request.user == user:
            #退出登录
            logout(request)
            #删除用户数据
            user.delete()
            #返回博客列表
            return redirect("article:article_list")
        else:
            return HttpResponse("你没有删除操作权限")
    else:
        return HttpResponse("仅接受post请求")

#编辑用户信息
@login_required(login_url='/userprofile/login/')
def profile_edit(request,id):
    #根据id获取需要修改的用户对象
    user = User.objects.get(id=id)
    #user_id是OneToOneField自动生成的字段
    #根据此字段获取user对应的信息
    profile = Profile.objects.get(user_id=id)

    if request.method == 'POST':
        #验证修改数据的用户是不是被修改的用户
        if request.user != user:
            return HttpResponse("你没有权限修改此用户信息")
        # 上传的文件保存在 request.FILES 中，通过参数传递给表单类
        profile_form = ProfileForm(request.POST,request.FILES)
        #如果数据合法
        if profile_form.is_valid():
            #得到清洗数据
            profile_cd = profile_form.cleaned_data
            #获取各属性值
            profile.phone = profile_cd['phone']
            profile.bio = profile_cd['bio']
            # 如果 request.FILES 存在键为avatar的数据，则获取该数据
            if 'avatar' in request.FILES:
                profile.avatar = profile_cd["avatar"]
            profile.save()
            #带参数的redirect
            return redirect("userprofile:edit",id=id)
        else:
            return HttpResponse("表单输入有误，请重新输入~")
    elif request.method == 'GET':
        profile_form = ProfileForm()
        context = {'profile_form':profile_form,'profile':profile,'user':user}
        return render(request,'userprofile/edit.html',context)
    else:
        return HttpResponse("请使用GET或POST请求数据")









