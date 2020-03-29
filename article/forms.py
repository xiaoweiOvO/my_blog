#form类，描述一张表单并决定如何工作及呈现

#引入表单类
from django import forms
#引入文章模型类
from .models import ArticlePost, ArticleColumn


#写文章的表单类
class ArticlePostForm(forms.ModelForm):
    class Meta:
        #指明数据模型来源
        model = ArticlePost
        #定义表单包含的字段
        fields = ('title','body','tags')

#栏目的表单类
class ArticleColumnForm(forms.ModelForm):
    class Meta:
        model = ArticleColumn
        fields = ('title',)
