# --*-- coding:utf-8 --*--
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask import Blueprint,render_template
from . import book_blue

class BookFrom(FlaskForm):
    """添加书籍信息表单类"""
    pass


#用蓝图实例对象中的route进行装饰
@book_blue.route('/books')
def books():
    #返回所有作者和对应的书籍
    return render_template('books.html')
