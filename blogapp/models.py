# -*- coding: utf-8 -*-
from django.db import models

class userInfo(models.Model):
    uid = models.AutoField(primary_key=True)
    username = models.CharField(verbose_name='用户名',max_length=32)
    nickname = models.CharField(verbose_name='昵称',max_length=32,default='exit')
    password = models.CharField(verbose_name='密码',max_length=64)
    email = models.EmailField(verbose_name='邮箱',unique=True)
    avatar = models.ImageField(verbose_name='头像')
    create_time = models.DateTimeField(verbose_name='注册时间',auto_now_add=True)

class Blog(models.Model):
    bid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='博客标题',max_length=64)
    site = models.CharField(verbose_name='个人博客链接',max_length=32,unique=True)
    theme = models.CharField(verbose_name='博客主题',max_length=32)
    user = models.OneToOneField(to=userInfo,to_field='uid',on_delete=models.CASCADE)








