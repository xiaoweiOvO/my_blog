from article.models import ArticlePost
from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.
# django-mptt
from mptt.models import MPTTModel, TreeForeignKey


#评论类 旧版普通评论类 为实现树形评论结构 不再使用
'''
class Comment(models.Model):
    #评论的文章属性,使用关联外键文章类,需要导入文章类
    article = models.ForeignKey(ArticlePost,on_delete=models.CASCADE,related_name='comments')
    #评论者,使用关联外键用户类,需要导入用户类
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    #评论正文改用服务本编辑器字段
    #body = models.TextField()
    body = RichTextField()
    #评论时间
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.body[:20]
'''

#评论类 实现树形结构的评论
class Comment(MPTTModel):
    # 评论的文章属性,使用关联外键文章类,需要导入文章类
    article = models.ForeignKey(ArticlePost, on_delete=models.CASCADE, related_name='comments')
    # 评论者,使用关联外键用户类,需要导入用户类
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    # 评论正文改用富文本字段
    # body = models.TextField()
    body = RichTextField()
    #评论时间
    created = models.DateTimeField(auto_now_add=True)
    #mptt树形结构
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    #记录二级评论回复给谁, str
    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyers'
    )

    # 替换 Meta 为 MPTTMeta
    class MPTTMeta:
        order_insertion_by = ['created']

    def __str__(self):
        return self.body[:20]














