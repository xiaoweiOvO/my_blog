#引入表单类
from django import forms
#引入User模型
from django.contrib.auth.models import User

#用户登录表单,继承了forms.Form类 适用于不于数据库进行直接交互的功能
#而文章表单继承的forms.ModelForm适用于需要直接与数据库交互的功能
from .models import Profile


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

#用户注册表单类
class UserRegisterForm(forms.ModelForm):
    #输入两次密码
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username','email')

    #对两次输入的密码检查是否一致 clean_**方法django会自动调用
    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError('密码输入不一致，请重新输入')

#用户扩展信息表单类
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone','avatar','bio')