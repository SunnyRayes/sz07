# --*-- coding:utf-8 --*--
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask import render_template, request, flash, redirect, url_for
from manage import Book,Author,db
from . import book_blue
from apps.author import author_blue

class BookFrom(FlaskForm):
    """添加书籍信息表单类"""
    author=StringField(u'作者：',validators=[DataRequired()])
    book=StringField(u'书籍：',validators=[DataRequired()])
    submit=SubmitField(u'添加')


#用蓝图实例对象中的route进行装饰
@book_blue.route('/books',methods=['GET','POST'])
def books():
    #表单
    book_form = BookFrom()
    #POST请求，添加书籍
    if request.method=='POST':
        #校验数据
        if not book_form.validate_on_submit():
            #获取作者名书名
            author_name=request.form.get('author')
            book_name=request.form.get('book')
            author=Author.query.filter(Author.name==author_name).first()
            #判断作者是否已存在，存在
            if author:
                #判断书籍是否存在:
                book=Book.query.filter(Book.author_id==author.id,Book.name==book_name).first()
                if book:
                    flash(u'书籍存在')
                else:   #书籍不存在，添加
                    book=Book(name=book_name,author_id=author.id)
                    try:
                        db.session.add(book)
                        db.session.commit()
                    except Exception as e:
                        print e
                        #回滚
                        db.session.rollback()
                        flash(u'添加失败')
            else:
                #新增作者，书名
                author=Author(name=author_name)
                book=Book(name=book_name,author_id=author.id)
                #绑定了书籍作者关系
                book.author=author
                try:
                    #添加书籍即可
                    db.session.add(book)
                    db.session.commit()
                except Exception as e:
                    print e
                    #回滚
                    db.session.rollback()
                    flash(u'添加书籍和作者失败')
        else:
            flash(u'数据不完整')

    #get请求返回所有作者和对应的书籍
    authors=Author.query.all()
    return render_template('books.html',form=book_form,authors=authors)

#删除书籍视图函数
@book_blue.route('/del_book/<int:book_id>')
def del_book(book_id):
    #判断是否为空
    if book_id:
        #获取书籍的id
        book=Book.query.get(book_id)
        if book:
            try:
                db.session.delete(book)
                db.session.commit()
            except Exception as e:
                print e
                db.session.rollback()
                return e
            #获取书籍
            books =Book.query.filter(Book.author_id==book.author_id)
            #如果该作者没有书籍了，则删除
            if len(books.all())==0:
                author=Author.query.get(book.author_id)
                try:
                    db.session.delete(author)
                    db.session.commit()
                except Exception as e :
                    print e
                    db.session.rollback()
            return redirect('/books')
    else:
        return u'数据为空！删除失败，'



#删除作者
@author_blue.route('/del_author/<int:author_id>')
def del_author(author_id):
    if author_id:
        #删除作者的所有的书籍
        author=Author.query.get(author_id)
        if author:
            books=Book.query.filter(Book.author_id==author.id).all()
            try:
                for book in books:
                    db.session.delete(book)
                db.session.delete(author)
                db.session.commit()
            except Exception as e :
                print e
                db.session.rollback()
                return u'删除作者失败'
            return redirect('/books')
        return u'没有该作者'
        #删除作者
    return u'数据错误'
