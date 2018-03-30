# --*-- coding:utf-8 --*--
from manage import db

class Author(db.Model):
    """作者模型类"""
    __tablename__='authors'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True)
    #定义关联查询的关系
    books=db.relationship('apps.book.Book',backref='author',lazy='dynamic')


class Book(db.Model):
    """图书模型类:一"""
    __tabelname='books'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True)
    author_id=db.Column(db.Integer,db.ForeignKey(Author.id))