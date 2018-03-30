# --*-- coding:utf-8 --*--
#d导入flask包
from flask import Flask
#导入orm框架
from flask_sqlalchemy import SQLAlchemy
#管理器类,添加脚本命令
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
#导入蓝图
from apps.author import author_blue
from apps.book import book_blue
#创建应用
app=Flask(__name__)
#注册蓝图
app.register_blueprint(book_blue)
app.register_blueprint(author_blue)
# 引入配置文件
app.config.from_pyfile('config.conf')
#管理器
manager=Manager(app)
#数据库连接
db=SQLAlchemy(app)
#1.迁移命令,绑定应用程序，数据库实例对象
migrate=Migrate(app,db)
#2.添加迁移命令到脚本，命令名为db。
manager.add_command('db',MigrateCommand)

class Author(db.Model):
    """作者模型类"""
    __tablename__='authors'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True)
    #定义关联查询的关系
    books=db.relationship('Book',backref='author',lazy='dynamic')


class Book(db.Model):
    """图书模型类:一"""
    __tabelname='books'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True)
    author_id=db.Column(db.Integer,db.ForeignKey(Author.id))

@app.route('/index',methods=['GET'])
def index():
    return 'index'

#3.python manage.py db init 创建migrations迁移文件夹
#4.python manage.py db migrate -m 'first_migrate' m是版本描述
if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    # 生成数据
    au1 = Author(name=u'老王')
    au2 = Author(name=u'老尹')
    au3 = Author(name=u'老刘')
    # 把数据提交给用户会话
    db.session.add_all([au1, au2, au3])
    # 提交会话
    db.session.commit()
    bk1 = Book(name=u'老王回忆录', author_id=au1.id)
    bk2 = Book(name=u'我读书少，你别骗我', author_id=au1.id)
    bk3 = Book(name=u'如何才能让自己更骚', author_id=au2.id)
    bk4 = Book(name=u'怎样征服美丽少女', author_id=au3.id)
    bk5 = Book(name=u'如何征服英俊少男', author_id=au3.id)
    # 把数据提交给用户会话
    db.session.add_all([bk1, bk2, bk3, bk4, bk5])
    # 提交会话
    db.session.commit()
    manager.run()
