from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from article.models import ArticlePost

#通知列表的 类视图  #继承自ListView  用于展示所有的未读通知
#继承了"混入类"LoginRequiredMixin，要求调用此视图必须先登录
class CommentNoticeListView(LoginRequiredMixin,ListView):
    #上下文名称
    context_object_name = 'notices'
    #模板位置
    template_name = 'notice/list.html'
    #登录重定向
    login_url = '/userprofile/login/'

    #未读通知的查询集
    def get_queryset(self):
        #返回了传递给模板的上下文对象
        #unread()方法是django-notifications提供的，用于获取所有未读通知的集合
        return self.request.user.notifications.unread()

#更新通知状态
#继承自View
class CommentNoticeUpdateView(View):
    #处理get请求
    def get(self,request):
        #获取未读通知
        notice_id = request.GET.get('notice_id')
        #更新单条通知
        if notice_id:
            article = ArticlePost.objects.get(id=request.GET.get('article_id'))
            #将未读通知转换为已读
            request.user.notifications.get(id=notice_id).mark_as_read()
            return redirect(article)
        #更新全部通知
        else:
            #将全部未读通知转换为已读
            request.user.notifications.mark_all_as_read()
            return redirect('notice:list')






















