# -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import Wheel,Nav,Handletypes,Pic,User
import time
import os

# Create your views here.
def home(request):
   wheelsList = Wheel.objects.all()
   navList1 = Nav.objects.filter(trackid__lte=4)
   navList2 = Nav.objects.filter(trackid__gt=4)
   return render(request,'web_img_enhancement/home.html',{"Title":"主页",
                "wheelsList":wheelsList,"navList1":navList1,"navList2":navList2})

def handle(request,trackid):
   leftSlider = Handletypes.objects.all()
   Type = Handletypes.objects.get(trackid=trackid)
   return render(request,'web_img_enhancement/handle.html',{"Title":"结果管理",
                    "leftSlider":leftSlider,"Type":Type})


def exhibit(request,trackid):
   user_Account = ''
   token = request.session.get("token")
   print(token)
   if token == None:
      request.session["status"] = "您还没有登录,请先登录"
   else:
      user = User.objects.get(userToken=token)
      user_Account = user.userAccount
   Type = Handletypes.objects.get(trackid=trackid)
   try:
      result = Pic.objects.filter(isdelete=0,type=trackid,userAccount=user_Account)
   except Pic.DoesNotExist as e:
      return render(request, 'web_img_enhancement/exhibit.html', {"Title": "结果展示", "Type": Type})
   return render(request,'web_img_enhancement/exhibit.html',{"Title":"结果展示","Type":Type,
                           "resultsList":result})

def mine(request,flag):
   username = request.session.get("username", "点击登录")
   usertoken = request.session.get("token")
   if flag == '0':
      return render(request,'web_img_enhancement/mine.html',{"Title":"我的","username":username})
   if flag == '1':
      if usertoken!= None:
         user = User.objects.get(userToken = usertoken)
         user_Account = user.userAccount
         try:
            result = Pic.objects.filter(isdelete=0, userAccount=user_Account)
            return render(request,'web_img_enhancement/mine.html',{"Title":"我的","username":username,"resultsList":result})
         except Pic.DoesNotExist as e:
            return render(request,'web_img_enhancement/mine.html',{"Title":"我的","username":username,"resultsList":result})
      else:
         return redirect('/mine/0/')
   if flag == '2':
      if usertoken != None:
         user = User.objects.get(userToken=usertoken)
         user_Account = user.userAccount
         try:
            result = Pic.objects.filter(isdelete=0, userAccount=user_Account,iscollect=1)
            return render(request, 'web_img_enhancement/mine.html',
                          {"Title": "我的", "username": username, "resultsList": result})
         except Pic.DoesNotExist as e:
            return render(request, 'web_img_enhancement/mine.html',
                          {"Title": "我的", "username": username, "resultsList": result})
      else:
         return redirect('/mine/0/')
   if flag == '3':
      if usertoken != None:
         user = User.objects.get(userToken=usertoken)
         user_Account = user.userAccount
         user_name = user.userName
         user_Phone = user.userPhone
         user_Address = user.userAdderss
         return render(request, 'web_img_enhancement/mine.html',
                  {"Title": "我的", "username": username, "useraccount":user_Account,
                  "username":user_name,"userphone":user_Phone,"useraddress":user_Address})
      else:
         return redirect('/mine/0/')
   if flag == '4':
      if usertoken != None:
         user = User.objects.get(userToken=usertoken)
         user_Account = user.userAccount
         try:
            result = Pic.objects.filter(isdelete=1, userAccount=user_Account)
            return render(request, 'web_img_enhancement/mine.html',
                          {"Title": "我的", "username": username, "resultsList": result})
         except Pic.DoesNotExist as e:
            return render(request, 'web_img_enhancement/mine.html',
                          {"Title": "我的", "username": username, "resultsList": result})
      else:
         return redirect('/mine/0/')
   if flag == '5' or flag == '6':
         return render(request,'web_img_enhancement/mine.html',{"Title":"我的","username":username})

#要上传文件了,需要引入下面这些
from django.http import HttpResponse
from django.conf import settings
import os
from .method import AGCWD,quwu,lashen,jiami,mohu,ruihua,shibie,quzao,trans
from django.shortcuts import redirect

def sc(request):
   return render(request,'web_img_enhancement/sc.html')

def sctp(request,trackid):
   token = request.session.get("token")
   print(token)
   if token == None:
      request.session["status"] = "您还没有登录,请先登录"
      return redirect('/handle/'+trackid+'/')
   if request.method == 'POST':
      user = User.objects.get(userToken=token)
      if trackid != '3':
         pic_name = request.POST.get('pic_name')
         pic_obj = request.FILES.get('picture')
         #上传图片到服务器中
         pic = os.path.join(settings.MEDIA_ROOT, pic_name + ".png")
         pic_res = os.path.join(settings.MEDIA_ROOT, pic_name +"_result"+ ".png")
         with open(pic, "wb") as fp:
            for data in pic_obj.chunks():
               fp.write(data)
         #将图片存到数据库中(结果路径也已经先存入了)
         picture = Pic()
         picture.name = pic_name
         picture.abs_path = pic
         picture.rel_path = '/static/media/'+ pic_name +'.png'
         picture.res_path = '/static/media/'+ pic_name +"_result.png"
         picture.type = trackid
         picture.userAccount = user.userAccount
         picture.save()
         # 针对性的来进行图片结果的操作
         if trackid == '1':
            AGCWD(picture.abs_path.replace('\\','\\\\'),pic_res)
         elif trackid == '2':
            quwu(picture.abs_path.replace('\\','\\\\'),pic_res)
         elif trackid == '4':
            lashen(picture.abs_path.replace('\\','\\\\'),pic_res)
         elif trackid == '5':
            jiami(picture.abs_path.replace('\\','\\\\'),pic_res)
         elif trackid == '6':
            mohu(picture.abs_path.replace('\\','\\\\'),pic_res)
         elif trackid == '7':
            ruihua(picture.abs_path.replace('\\','\\\\'),pic_res)
         elif trackid == '8':
            shibie(picture.abs_path.replace('\\','\\\\'),pic_res)
         elif trackid == '9':
            quzao(picture.abs_path.replace('\\','\\\\'),pic_res)

         redirect_path = '/handle/' + trackid + '/'
         request.session["res_path"] = picture.res_path
      else:
         pic_name = request.POST.get('pic_name')
         pic_yuan_obj = request.FILES.get('picture')
         pic_canzhao_obj = request.FILES.get('picture2')
         # 上传图片到服务器中
         yuan_pic = os.path.join(settings.MEDIA_ROOT, pic_name + ".png")
         canzhao_pic = os.path.join(settings.MEDIA_ROOT, pic_name + "_reference.png")
         pic_res = os.path.join(settings.MEDIA_ROOT, pic_name + "_result" + ".png")
         with open(yuan_pic, "wb") as fp:
            for data in pic_yuan_obj.chunks():
               fp.write(data)
         with open(canzhao_pic, "wb") as fp:
            for data in pic_canzhao_obj.chunks():
               fp.write(data)
         #将图片存到数据库中(结果路径也已经先存入了)
         yuan_picture = Pic()
         yuan_picture.name = pic_name
         yuan_picture.abs_path = yuan_pic
         yuan_picture.rel_path = '/static/media/'+ pic_name +'.png'
         yuan_picture.res_path = '/static/media/'+ pic_name +"_result.png"
         yuan_picture.ref_rel_path = '/static/media/' + pic_name + "_reference.png"
         yuan_picture.type = trackid
         yuan_picture.userAccount = user.userAccount
         yuan_picture.save()
         trans(yuan_picture.abs_path.replace('\\', '\\\\'),canzhao_pic.replace('\\', '\\\\'), pic_res)
         redirect_path = '/handle/' + trackid + '/'
         request.session["res_path"] = yuan_picture.res_path
      return redirect(redirect_path)

from django.http import JsonResponse
def check(request, flag):
   print(flag)
   token = request.session["token"]
   try:
      user = User.objects.get(userToken=token)
      user_account = user.userAccount
   except User.DoesNotExist as e:
      pass
   if flag == '0':
      print("保存成功")
      del request.session["res_path"]
      return JsonResponse({"data": -2, "status": "success"})
   if flag == '1':
      pic = Pic.objects.get(res_path=request.session["res_path"],isdelete=0)
      print(pic)
      pic.isdelete = 1
      pic.save()
      del request.session["res_path"]
      print("删除成功")
      return JsonResponse({"data": -1, "status": "success"})
   if flag == '2':
      # ajax发过来数据用POST来取,去我们对应的表里取数据,能取出来就说明该名称已经被使用了
      getname = request.POST.get("name")
      #先使用session拿出该用户的所有数据-----未做
      #
      #
      #
      #
      try:
         pic = Pic.objects.get(name = getname,userAccount = user_account)
         # 这是取到了不能命名  这个被ajax的data接收  这个被status接收
         return JsonResponse({"data": "该名称已经被使用啦", "status": "error"})
      except Pic.DoesNotExist as e:
         # 用get去取数据发生的异常---一种是不存在,一种是取了多个
         # 这是没取到 能注册
         return JsonResponse({"data": "ok!!!niubi", "status": "success"})

def manipulate(request,flag):
   if flag == '0':
      pid = request.POST.get("bianhao")
      pic = Pic.objects.get(id=pid)
      pic.isdelete = 1
      pic.save()
      return JsonResponse({"data": -1, "status": "success"})
   if flag == '1':
      print("我进来啦！")
      pid = request.POST.get("bianhao")
      name = request.POST.get("newname")
      try:
         old_pic = Pic.objects.get(name=name)
         print(old_pic)
         return JsonResponse({"data": -1, "status": "fail"})
      except Pic.DoesNotExist as e:
         pic = Pic.objects.get(id=pid)
         pic.name = name
         pic.save()
         return JsonResponse({"data": -1, "status": "success"})
   if flag == '2':
      print("我进来修改了！")
      pid = request.POST.get("bianhao")
      pic = Pic.objects.get(id=pid)
      pic.iscollect = 1
      pic.save()
      return JsonResponse({"data": -1, "status": "success"})
   if flag == '3':
      print("我来取消收藏了")
      pid = request.POST.get("bianhao")
      pic = Pic.objects.get(id=pid)
      pic.iscollect = 0
      pic.save()
      return JsonResponse({"data": -1, "status": "success"})
   if flag == '4':
      print("我来恢复图像了")
      pid = request.POST.get("bianhao")
      pic = Pic.objects.get(id=pid)
      pic.isdelete = 0
      pic.save()
      return JsonResponse({"data": -1, "status": "success"})


import time
import random
def register(request):
   if request.method == 'POST':
      userAccount = request.POST.get("userAccount")
      userPasswd = request.POST.get("userPass")
      userName = request.POST.get("userName")
      userPhone = request.POST.get("userPhone")
      userAdderss = request.POST.get("userAdderss")
      # 让时间戳加上随机数,就算有人同时注册,也可以保证他们是不一样的
      token = time.time() + random.randrange(1, 100000)
      # 现在拿到的是数字类型的,把他变成字符串类型
      userToken = str(token)
      # 注意图片不是从POST里拿,是从FILES里拿,相当拿到的文件描述符
      f = request.FILES["userImg"]
      # 头像是要上传的,所以直接拿是不对的,要把他和settings下的MEDIA_ROOT结合
      # 用userAccount.png上传,防止图片名重复
      userImg = os.path.join(settings.MEDIA_ROOT, userAccount + ".png")
      with open(userImg, "wb") as fp:
         for data in f.chunks():
            fp.write(data)
      userImgpath = "/static/media/"+userAccount+".png"
      # 创建user对象,把数据存到数据库中！
      user = User.createuser(userAccount, userPasswd, userName, userPhone, userAdderss, userImgpath,userToken)
      user.save()
      # 注册好后把信息存到了session里,为了状态保持显示用户名的
      request.session["username"] = userName
      request.session["token"] = userToken
      request.session["userimg"] = userImgpath
      request.session["status"] = None
      return redirect('/mine/0/')
   else:
      return render(request, 'web_img_enhancement/register.html', {"Title": "注册"})


def login(request):
   if request.method == "POST":
      print("***********")
      nameid = request.POST.get("username")
      pswd = request.POST.get("password")
      print("name=", nameid)
      print("pswd=", pswd)
      try:
         user = User.objects.get(userAccount=nameid)
         if user.userPasswd != pswd:
            # 返回错误信息
            print("密码错了")
            return render(request, 'web_img_enhancement/login.html', {"Title": "登陆", "error": "密码错误"})
      except User.DoesNotExist:
            # 返回错误信息
            return render(request, 'web_img_enhancement/login.html', {"Title": "登陆", "error": "该用户不存在"})
      # 登录成功,生成一个token
      # 让时间戳加上随机数,就算有人同时注册,也可以保证他们是不一样的
      token = time.time() + random.randrange(1, 100000)
      # 现在拿到的是数字类型的,把他变成字符串类型并且把用户的token值换掉
      user.userToken = str(token)
      user.save()  # 重新save这个user(其实是更改update)

      # 把session存一下
      request.session["username"] = user.userName
      request.session["userimg"] = user.userImg
      request.session["token"] = user.userToken
      request.session["status"] = None
      return redirect('/mine/0/')
   else:  # 第一次点未登录不走上面的if走的是这里,显示表单
      return render(request, 'web_img_enhancement/login.html', {"Title": "登陆"})

#退出登录
from django.contrib.auth import logout
def quit(request):
    logout(request)
    return JsonResponse({"data": -1, "status": "success"})


def checkuserpsd(request):
   # ajax发过来数据用POST来取,去我们对应的表里取数据,能取出来就说明已经被注册了
   useraccount = request.POST.get("useraccount")
   userpswd = request.POST.get("userpsd")
   user = User.objects.get(userAccount=useraccount)
   if user.userPasswd == userpswd:
      return JsonResponse({"data": "ok!!!niubi", "status": "success"})
   else:
      return JsonResponse({"data": "密码不一致", "status": "error"})

def checkuserid(request):
   # ajax发过来数据用POST来取,去我们对应的表里取数据,能取出来就说明已经被注册了
   userid = request.POST.get("userid")

   try:
      user = User.objects.get(userAccount=userid)
      # 这是取到了不能注册  这个被ajax的data接收  这个被status接收
      return JsonResponse({"data": "该用户已经被注册啦", "status": "error"})
   except User.DoesNotExist as e:
      # 用get去取数据发生的异常---一种是不存在,一种是取了多个
      # 这是没取到 能注册
      return JsonResponse({"data": "ok!!!niubi", "status": "success"})

def modify(request):
   token = request.session.get("token")
   print(token)
   if token == None:
      username = request.session.get("username", "点击登录")
      return redirect('/mine/0/')
   token = request.session.get("token")
   user = User.objects.get(userToken=token)
   if request.method == 'POST':
      f = None
      userAccount = user.userAccount
      userName = request.POST.get("userName")
      if user.userName!=userName:
         user.userName=userName
         user.save()
      userPhone = request.POST.get("userPhone")
      if user.userPhone!=userPhone:
         user.userPhone=userPhone
      userAdderss = request.POST.get("userAdderss")
      if user.userAdderss != userAdderss:
         user.userAdderss = userAdderss
      try:
         f = request.FILES["userImg"]
      except :
         print("没有值")
      if f!=None:
         # 头像是要上传的,所以直接拿是不对的,要把他和settings下的MEDIA_ROOT结合
         # 用userAccount.png上传,防止图片名重复
         userImg = os.path.join(settings.MEDIA_ROOT, userAccount + ".png")
         #先删除头像的原文件
         print(userImg)
         try:
            os.remove(userImg)
         except OSError as e:
            print('没删除成功！！！！')
         with open(userImg, "wb") as fp:
            for data in f.chunks():
               fp.write(data)
         userImgpath = "/static/media/"+userAccount+".png"
         request.session["userimg"] = userImgpath
      user.save()
      # 注册好后把信息存到了session里,为了状态保持显示用户名的
      request.session["username"] = userName
      request.session["status"] = None
      return redirect('/mine/0/')
   else:
      userAccount = user.userAccount
      userName = user.userName
      userPhone = user.userPhone
      userAddress = user.userAdderss
      userImg = user.userImg
      return render(request, 'web_img_enhancement/modify.html', {"Title": "编辑信息",
             "Ac":userAccount,"Na":userName,"Ph":userPhone,"Ad":userAddress,"Img":userImg})


def security(request):
   token = request.session.get("token")
   print(token)
   if token == None:
      #username = request.session.get("username", "点击登录")
      return redirect('/mine/0/')
   user = User.objects.get(userToken=token)
   userAccount = user.userAccount
   if request.method == 'POST':
      user_newpswd = request.POST.get("newpswd2")
      user.userPasswd = user_newpswd
      user.save()
      logout(request)
      time.sleep(1.5)
      return redirect('/mine/0/')
   else:
      return render(request, 'web_img_enhancement/security.html', {"Title": "账号管理"
         ,"Ac":userAccount})