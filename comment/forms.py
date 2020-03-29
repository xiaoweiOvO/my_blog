from django import forms
from .models import Comment

#表单类    这里需要导入django的表单类
class CommentForm(forms.ModelForm):
    #定义元数据
    class Meta:
        #这里需要导入评论模型类
        model = Comment
        fields = ['body']