from comment.models import Comment
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

#引入文章模型类
from article.models import ArticlePost,ArticleColumn,likes
#引入markdown库
import markdown
#引入分页模块
from django.core.paginator import Paginator
#引入django内部的views模块
from django.views import View
#引入评论表单类
from comment.forms import CommentForm

#类视图
class ArticleListView(View):
    """处理get请求"""
    def get(self,request):
        articles = ArticlePost.objects.all()
        context = {'article':articles}
        return render(request,'article/list.html',context)

#文章列表的视图函数(旧，不再使用)
'''
def article_list(request):
    # 根据GET请求中查询条件
    # 返回不同排序的对象数组
    if request.GET.get('order') == 'total_views':
        #获取所有文章按-total_views排序
        article_list = ArticlePost.objects.all().order_by('-total_views')
        #设置排序的名称
        order = 'totla_views'
    else:
        #默认排序
        article_list = ArticlePost.objects.all()
        order = 'normal'
    #每页显示2篇文章
    paginator = Paginator(article_list,3)
    #获取url中的页码  在url的末尾加上?key=value的键值对,request.GET.get('key')
    page = request.GET.get('page')
    #将页码对应的文章返回给articles
    articles = paginator.get_page(page)
    #需要传递给模板的对象，字典格式
    context = {'articles':articles,'order':order}
    #render函数：载入模板并返回context对象
    #参数，request    固定的request对象
    #     article/list.html  模板文件的路径
    #     coontext    传递到模板的数据
    return  render(request,'article/list.html',context)
'''

# 引入 Q 对象
from django.db.models import Q
#文章列表的视图函数(新,包含简单的搜索和排序功能)
def article_list(request):
    #获取GET请求中的search和order等查询参数数据
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')
    #初始化查询集
    article_list = ArticlePost.objects.all()
    '''
    #如果search存在
    if search:
        #如果排序方式为浏览量
        if order == 'total_views':
            # 用Q对象进行联合搜索
            #搜索标题或正文包含search的文章列表,并排序
            #icontains查询不区分大小写
            #contains查询区分大小写
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            ).order_by('-total_views')
        else:
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    #search不存在,表示当前没有搜索操作search=null
    else:
        # 将search参数重置为空
        search = ''
        #判断是否排序
        if order == 'total_views':
            article_list = ArticlePost.objects.all().order_by('-total_views')
        else:
            article_list = ArticlePost.objects.all()
    '''
    #搜索查询集
    if search:
        article_list = article_list.filter(
            Q(title__icontains=search)|
            Q(body__icontains=search)
        )
    else:
        search=''

    #栏目查询集
    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)

    #标签查询集
    if tag and tag != 'None':
        #django-taggit中标签过滤的写法
        article_list = article_list.filter(tags__name__in = [tag])

    #查询集排序
    if order == 'total_views':
        article_list = article_list.order_by('-total_views')

    paginator = Paginator(article_list, 3)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    #将需要返回的数据赋值给context
    context = {
        'articles':articles,
        'order':order,
        'search':search,
        'column':column,
        'tag':tag,
    }
    return render(request, 'article/list.html', context)

#文章详情
def article_detail(request,id):
    #根据id取出相应的文章
    article = ArticlePost.objects.get(id = id)
    # 获取该文章的评论  filter可以查询多个对象而get只能查询一个对象
    comments = Comment.objects.filter(article=id)
    # 每次调用某文章详情页则浏览量字段+1并保存
    article.total_views += 1
    #update_fields=[]指定了数据库只更新total_views特定字段，优化执行效率
    article.save(update_fields=['total_views'])
    #点赞数
    likelist = likes.objects.filter(article=article)
    likenum = likelist.count()
    #当前用户是否点赞
    like = likes.objects.filter(Q(article=id) | Q(user=request.user.id))
    if like:
        islike = True
    else:
        islike = False

    #markdown.markdown语法接收两个参数：
    #第一个参数是需要渲染的文章正文article.body；
    #第二个参数载入了常用的语法扩展，markdown.extensions.extra中包括了缩写、表格等扩展，
    #markdown.extensions.codehilite则是后面要使用的代码高亮扩展。
    #代码块语法如下(语法错误会导致输出格式有问题):
    #```Python
    #代码内容
    #```
    #将markdown语法渲染成html样式
    #只能在文章中使用自动生成目录,不够实用
    '''
    article.body = markdown.markdown(article.body,
            extensions=[
                #包含缩写，表格等常用扩展
                'markdown.extensions.extra',
                #语法高亮扩展
                'markdown.extensions.codehilite',
                #目录扩展
                'markdown.extensions.toc',#在文章中的任意位置插入[TOC]字符串,自动生成目录
            ])
    '''
    #修改后可以在页面内使用目录
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    #使用convert方法将正文渲染成html页面，通过md.toc将目录传递给模板
    article.body = md.convert(article.body)
    #引入评论表单
    comment_form = CommentForm()
    #需要传递给模板的对象，字典格式
    context = {'article':article,'toc':md.toc, 'comments': comments,'comment_form':comment_form,'likes':likenum,'islike':islike}
    #返回模板context对象
    return render(request,'article/detail.html',context)

#引入文章的form类
from .forms import ArticlePostForm, ArticleColumnForm
#引入User模型类
from django.contrib.auth.models import User

#新建栏目
@login_required(login_url='account_login')
def column_create(request):
    if request.method == "POST":
        article_column_form = ArticleColumnForm(request.POST)
        if article_column_form.is_valid():
            new_column = article_column_form.save(commit=False)
            new_column.author = User.objects.get(id=request.user.id)
            new_column.save()
            return redirect("article:article_create")
        else:
            return HttpResponse("表单内容有误请重新填写")
    else:
        article_column_form = ArticleColumnForm()
        context = {"article_column_form":article_column_form}
        return render(request,'article/create_column.html',context)

#写文章的视图
@login_required(login_url='account_login')
def article_create(request):
    #判断用户是否提交数据POST请求还是获取数据GET请求
    '''
    如果是POST提交数据，将post提交的表单赋值给article_post_form实例
    使用jdango内置方法 .is_valid()判断提交的数据是否符合模型的要求
    '''
    if request.method == "POST":
        #定义表单实例article_post_form并赋值data=request.POST,用户提交的数据
        article_post_form = ArticlePostForm(request.POST)
        #判断实例对象是否满足模型的要求
        if article_post_form.is_valid():
            #保存数据，暂时不提交到数据库commit=False
            new_article = article_post_form.save(commit=False)
            #指定id为1的User对象为作者
            #new_article.author = User.objects.get(id=1)
            #指定当前登录用户为作者
            new_article.author = User.objects.get(id=request.user.id)
            #如果文章的栏目数据存在
            if request.POST['column'] != 'none':
                #设置文章的栏目
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            #将新文章保存到数据库中
            new_article.save()
            #保存tags的多对多关系
            article_post_form.save_m2m()
            #完成后返回文章列表      重定向操作
            return redirect("article:article_list")
        #如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误请重新填写")
    #如果是POST请求数据，返回一个空的表单类对象，提供给用户填写
    else:
        #创建表单类实例
        article_post_form = ArticlePostForm()
        #获取当前用户的所有栏目
        columns = ArticleColumn.objects.filter(author=request.user.id)
        #赋值上下文用于返回
        context = {'article_post_form':article_post_form,'columns':columns}
        #返回给模板
        return render(request,'article/create.html',context)

#删除文章(不安全) 这个函数不再调用
def article_delete(request,id):
    #根据id获取需要删除的文章对象
    article = ArticlePost.objects.get(id=id)
    #调用.delete()方法删除文章
    article.delete()
    #完成删除后返回文章列表
    return redirect("article:article_list")

@login_required(login_url='account_login')
#安全删除
def article_safe_delete(request,id):
    #根据id获取要删除的文章对象
    article = ArticlePost.objects.get(id=id)
    #判断删除请求发起者与文章作者是否相符,不相符则不允许删除
    if request.user != article.author:
        return HttpResponse("抱歉，你无权删除这篇文章。")
    if request.method == 'POST':
        #article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect("article:article_list")
    else:
        #只有携带csrf令牌的post请求才能被执行
        #所有post请求的csrf校验由django中间件实现
        return HttpResponse('仅允许post请求')

#修改文章
@login_required(login_url='/userprofile/login/')
def article_update(request,id):
    #获取需要修改的文章对象
    article = ArticlePost.objects.get(id=id)
    #如果提交请求的user不是文章的作者,不提供修改权限
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")
    #判断是否为POST提交表单数据
    if request.method == 'POST':
        #将提交的数据复制到文章表单实例
        article_post_form = ArticlePostForm(data=request.POST)
        #判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            #获取新提交的title、body数据,并保存文章对象
            article.title = request.POST['title']
            article.body = request.POST['body']
            #栏目
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None
            article.save()
            #返回到修改后的文章详细页面
            return redirect("article:article_detail",id=id)
        #如果数据不合法,返回错误信息
        else:
            return HttpResponse("表单内容有误,请重新输入")
    #如果是GET请求获取数据 返回表单和文章数据用于组成编辑页面
    else:
        #创建表单类实例
        article_post_form = ArticlePostForm()
        #
        columns = ArticleColumn.objects.all()
        #赋值context
        context = {'article':article,'article_post_form':article_post_form,'columns':columns}
        #返回context给对应页面
        return render(request,'article/update.html',context)

#添加或删除一条点赞信息
def clicklike(request,article_id):
    #根据两个id值查询是否有对应的点赞信息
    like = likes.objects.filter(Q(article=article_id) | Q(user=request.user.id))
    if like:
        like.delete()
    else:
        article = ArticlePost.objects.get(id=article_id)
        like = likes(article=article,user=request.user)
        like.save()

    return redirect("article:article_detail",id=article_id)














