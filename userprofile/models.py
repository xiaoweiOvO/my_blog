from django.contrib.auth.models import User
from django.db import models

# Create your models here.

#用户扩展信息
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    #与User模型构成一对一的关系
    #关联外键   每个profile模型对应一个user模型,可以添加各种扩展信息,而不用对user表进行改动
    #on_delete参数当该表中的某条数据删除后，关联外键的操作
    #   models.CASCADE表示级联删除,删除一个表的某条数据后对应表的数据也删除
    #   models.SET_NULL表示,删除一个表的某条数据后另一个表的对应数据置空,字段要允许为空
    #   models.SET_DEFAULT,删除后置为默认值
    #   PROTECT 阻止前面的删除操作，报出ProtectedError异常
    #   DO_NOTHING 什么也不做
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')

    #电话号码
    phone = models.CharField(max_length=20,blank=True)
    #头像 图像字段需要第三方库pillow支持
    #ImageField字段不会存储图片本身，而仅仅保存图片的地址
    avatar = models.ImageField(upload_to="avatar/%Y%m%d/",blank=True)
    #个人简介
    bio = models.TextField(max_length=500,blank=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)

#信号接收函数,每当新建User实例时自动调用
#django包含信号调度程序,在框架中某些位置发生某种操作时,通知其他应用程序
#post_save是一个内置信号,在模型调用save方法后发出信号(信号中还带有相关的数据)
#装饰器receiver用于接收信号,这里表示接收User模型调用save方法时发出的信号
#接收到信号后执行后面的函数
@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

#两个函数都接收来自User的save信号
#根据函数的参数created来判断是创建用户还是修改用户信息
#post_save = ModelSignal(providing_args=["instance", "raw", "created", "using", "update_fields"],
#created不为空即为创建用户
#所有save情况都执行修改操作
@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()







