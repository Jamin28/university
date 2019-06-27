from app.exts import db
from app.models import Users,Posts
import os
from flask_script import Manager
from flask_migrate import MigrateCommand
from app import create_app


#创建app 参数 为环境名称 在 config中已经配置   默认是default
app = create_app(os.environ.get('FLASK_CONFIG') or 'default')

manager = Manager(app)
manager.add_command('db',MigrateCommand)

# 实现插入假数据，用于测试分页 python manager.py create_test_posts
@manager.command
def create_test_posts():
    for x in range(1, 255):
        title = '标题：%s' % x
        content = '内容： %s' % x
        posts = Posts(title=title,content=content)
        posts.uid = 1
        db.session.add(posts)
        db.session.commit()
    print('插入成功')

if __name__ == "__main__":
    manager.run()