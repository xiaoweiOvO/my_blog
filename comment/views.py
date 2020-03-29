from comment.models import Comment
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from article.models import ArticlePost
from .forms import CommentForm
from notifications.signals import notify
from django.contrib.auth.models import User
from django.http import JsonResponse

# 写文章评论
@login_required(login_url='account_login')
def post_comment(request, article_id, parent_comment_id=None):
    #根据id获取文章对象
    article = get_object_or_404(ArticlePost, id=article_id)
    # 处理 POST 请求 提交评论表单
    if request.method == 'POST':
        #获取提交的表单
        comment_form = CommentForm(request.POST)
        #判断表单信息是否合法
        if comment_form.is_valid():
            #保存表单对象,但不提交到数据库
            new_comment = comment_form.save(commit=False)
            #设置评论的其他字段,提交的表单只有评论本身,需要添加文章和用户
            new_comment.article = article
            new_comment.user = request.user
            # 二级回复
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                # 若回复层级超过二级，则转换为二级
                new_comment.parent_id = parent_comment.get_root().id
                # 被回复人
                new_comment.reply_to = parent_comment.user
                new_comment.save()
                # 给其他用户发送通知
                if not parent_comment.user.is_superuser:
                    notify.send(
                        request.user,
                        recipient=parent_comment.user,
                        verb='回复了你',
                        target=article,
                        action_object=new_comment,
                    )
                return JsonResponse({"code": "200 OK", "new_comment_id": new_comment.id})
            #保存到数据库
            new_comment.save()
            #给管理员发送通知
            if not request.user.is_superuser:
                notify.send(
                    request.user,
                    recipient=User.objects.filter(is_superuser=1),
                    verb='回复了你',
                    target=article,
                    action_object=new_comment,
                )
            # 新增代码，添加锚点
            redirect_url = article.get_absolute_url() + '#comment_elem_' + str(new_comment.id)
            # 修改redirect参数
            return redirect(redirect_url)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
            # 处理 GET 请求
    elif request.method == 'GET':
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
            'article_id': article_id,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'comment/reply.html', context)
    # 处理错误请求
    else:
        return HttpResponse("发表评论仅接受POST请求。")

#删除评论
@login_required(login_url='account_login')
def delete_comment(request,id):
    #根据id获取评论对象
    comment = Comment.objects.get(id = id)
    #获取此评论的文章对象
    article = comment.article
    #判断发起删除请求的用户是否为将要删除评论的用户或者是评论文章的作者
    if request.user != comment.user and request.user != comment.article.author:
        return HttpResponse("您没有删除此评论的权限")

    if request.method == 'POST':
        #comment = Comment.objects.get(id=id)
        comment.delete()
        return redirect(article)
    else:
        return HttpResponse("仅允许POST请求")



















