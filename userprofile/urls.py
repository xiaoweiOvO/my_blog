from django.urls import path
from . import views

app_name = 'userprofile'

urlpatterns = [
    # 用户登录
    path('login/', views.user_login, name='login'),
    #用户注册
    path('register/',views.user_register,name='register'),
    #退出登录
    path('logout/',views.user_logout,name='logout'),
    #注销账号
    path('delete/<int:id>/',views.user_delete,name='delete'),
    #用户信息
    path('edit/<int:id>/',views.profile_edit,name='edit'),
    #用户主页
    path('personal/<int:id>',views.user_personal,name='personal'),
    #点击关注按钮
    path('focus/<int:id>',views.clickfocus,name='focus'),

]