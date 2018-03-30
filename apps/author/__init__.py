# --*-- coding:utf-8 --*--
#导入蓝图
from flask import Blueprint
#创建蓝图对象
author_blue=Blueprint('author',__name__)
#方便manage.py在导入author_bule时，能够让views里面的蓝图注册路由可以被执行到
from apps.author import views
