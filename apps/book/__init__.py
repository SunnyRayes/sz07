# --*-- coding:utf-8 --*--
#导入蓝图
from flask import Blueprint
#创建蓝图对象
book_blue=Blueprint('book',__name__)
#方便manage.py在导入book_bule时，能够让views里面的蓝图注册路由可以被执行到
from apps.book import views
