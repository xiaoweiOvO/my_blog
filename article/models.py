from django.db import models
# 导入内建的User模型。
from django.contrib.auth.models import User
# timezone 用于处理时间相关事务。
from django.utils import timezone

from django.urls import reverse
#
from PIL import Image
#第三方库app标签
from taggit.managers import TaggableManager

#文章的栏目模型
class ArticleColumn(models.Model):
    #栏目标题
    title = models.CharField(max_length=100,blank=True)
    #创建时间
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class ArticlePost(models.Model):
    #文章作者，ForeignKey表示外键 user ，on_delete指定数据删除连带方式
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    #文章标题，字符串类型，最大长度为100
    title = models.CharField(max_length=100)
    #文章正文，大文本使用TextField字段
    body = models.TextField()
    #文章创建时间，default = timezone.now表示默认值为当前时间
    created = models.DateTimeField(default=timezone.now)
    #文章更新时间，每次数据更新自动写入系统当前时间
    updated = models.DateTimeField(auto_now=True)
    #文章浏览量  PositiveIntegerField正整数字段,初值设为0
    total_views = models.PositiveIntegerField(default=0)
    #文章栏目   关联外键栏目 栏目与文章一对多的关系
    column = models.ForeignKey(ArticleColumn,null=True,blank=True,on_delete=models.CASCADE,related_name='article')
    #文章标签
    tags = TaggableManager(blank=True)

    #内部类 class Meta用于给model定义元数据（元信息）
    class Meta:
        #db_table:定义数据表名，推荐使用小写字母，数据表名默认为**项目名_类名
        #ordering:对象的默认排序字段     加负号则代表倒叙
        ordering = ('-created',)

    #函数__str__定义当调用对象的str()方法时的返回值内容
    def __str__(self):
        #返回文章标题
        return self.title

    # 获取文章地址    使用reverse()方法返回文章详情页面的url，实现路由重定向
    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])