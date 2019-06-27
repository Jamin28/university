from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from app import app
from exts import db
from models import User,Question,Answer,Movie,Admin

manager = Manager(app)

#绑定数据库的db
migrate = Migrate(app,db)

#添加迁移脚本
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()