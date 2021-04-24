from django.db import models

# Create your models here.
class Pic(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    abs_path = models.CharField(max_length=100)
    rel_path = models.CharField(max_length=50)
    res_path = models.CharField(max_length=100)
    ref_rel_path = models.CharField(max_length=100,default="none")
    type = models.IntegerField()
    isdelete = models.BooleanField(default=False)
    iscollect = models.BooleanField(default=False)
    userAccount = models.CharField(max_length=30)

class Wheel(models.Model):
    img = models.CharField(max_length=60)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=20)

class Nav(models.Model):
    img = models.CharField(max_length=60)
    name = models.CharField(max_length=20)
    trackid = models.IntegerField()

class Handletypes(models.Model):
    trackid = models.IntegerField()
    name = models.CharField(max_length=20)

# 用户模型类
class User(models.Model):
    # 用户账号，要唯一
    userAccount = models.CharField(max_length=20,unique=True)
    # 密码
    userPasswd  = models.CharField(max_length=20)
    # 昵称
    userName    =  models.CharField(max_length=20)
    # 手机号
    userPhone   = models.CharField(max_length=20)
    # 地址
    userAdderss = models.CharField(max_length=100)
    # 头像路径
    userImg     = models.CharField(max_length=150)
    # touken验证值，每次登陆之后都会更新
    userToken   = models.CharField(max_length=50)
    @classmethod
    def createuser(cls,account,passwd,name,phone,address,img,token):
        u = cls(userAccount = account,userPasswd = passwd,userName=name,userPhone=phone,userAdderss=address,userImg=img,userToken=token)
        return u