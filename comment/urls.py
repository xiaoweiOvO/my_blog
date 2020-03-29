from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    # 发表评论 由于评论总是依赖于某一篇文章,评论的发表也需要文章的id
    path('post_comment/<int:article_id>/', views.post_comment, name='post_comment'),
    # 处理二级回复
    path('post_comment/<int:article_id>/<int:parent_comment_id>', views.post_comment, name='comment_reply'),
    #删除评论
    path('delete_comment/<int:id>/',views.delete_comment,name='delete_comment'),


]