"""
Django settings for my_blog project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*1ursin*zrq3^7^weouozt_7wlqpbp2@-&_23=k81-pun-se##'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #安装的第三方库app
    "password_reset",       #重置密码
    'taggit',               #标签
    'ckeditor',             #富文本编辑器
    'mptt',                 #树形数据结构，用于评论模型
    'notifications',        #通知
    #自定义的app
    'userprofile',          #用户扩展信息
    'article',              #文章
    'comment',              #评论
    'notice',               #通知

    # allauth 启动必须项
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # 可添加需要的第三方登录
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.weibo',
    'allauth.socialaccount.providers.weixin',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'my_blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #设置模板文件夹位置
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # allauth 启动必须项
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'my_blog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

#配置数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'my_blog',
        'USER':'root',
        'PASSWORD':'123456',
        'HOST':'localhost',
        'PORT': 3306,
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

#时区设置
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

#静态文件的配置
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    #静态文件的引用
    os.path.join(BASE_DIR,'static'),
)

#通过邮箱重置密码,系统邮箱配置
#SMTP服务器,简单邮件传输协议 只能发送邮件,不能接收邮件
EMAIL_HOST = 'smtp.qq.com'
#邮箱地址
EMAIL_HOST_USER = '2283940851@qq.com'
#邮箱密码
EMAIL_HOST_PASSWORD = 'vznnidqttqolecgg'
#发送邮件的端口
EMAIL_PORT = 25
#是否使用TLS
EMAIL_USE_TLS = True
#默认的发件人
DEFAULT_FROM_EMAIL = '2283940851@qq.com'

#媒体文件配置
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

#配置富文本编辑器
CKEDITOR_CONFIGS =  {
    #django-ckeditor默认使用default配置
    'default':{
        #编辑器宽度自适应
        'width':'auto',
        #高度设置
        'height':'250px',
        #tab键转换空格数
        'tabSpaces': 4,
        #工具栏风格
        'toolbar': 'Custom',
        #工具栏按钮
        'toolbar_Custom':[
            #表情 代码块
            ['Smiley','CodeSnippet'],
            #字体风格
            ['Bold','Italic','Underline','RemoveFormat','Blockquote'],
            #字体颜色
            ['TextColor','BGColor'],
            #链接
            ['Link','Unlink'],
            #列表
            ['NumberedList','BulletedList'],
            #最大化
            ['Maximize']
        ],
        #加入代码块插件 添加 Prism 相关插件
        'extraPlugins': ','.join(['codesnippet', 'prism', 'widget', 'lineutils']),
    }
}

X_FRAME_OPTIONS = 'SAMEORIGIN'

AUTHENTICATION_BACKENDS = (
    # Django 后台可独立于 allauth 登录
    'django.contrib.auth.backends.ModelBackend',

    # 配置 allauth 独有的认证方法，如 email 登录
    'allauth.account.auth_backends.AuthenticationBackend',
)

# 设置站点
SITE_ID = 1

# 登录成功后重定向地址
LOGIN_REDIRECT_URL = '/'

#配置日志
LOGGING = {
    #配置版本
    'version': 1,
    #是否禁止默认配置的记录器
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            #DEBUG级别会包含所有的数据库查询记录
            #'level': 'DEBUG',
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/debug.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}











