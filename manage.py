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

@app.route('/index',methods=['GET'])
def index():
    return 'index'

#3.python manage.py db init 创建migrations迁移文件夹
#4.python manage.py db migrate -m 'first_migrate' m是版本描述
if __name__ == '__main__':
    print app.url_map
    # from models import Author, Book
    manager.run()
