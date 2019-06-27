import os
base_dir = os.path.abspath(os.path.dirname(__file__))
class Config:

    #每页显示多少条数据
    PERPAGE_NUM = 3

    #密钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'jiangxiligong'
    #数据库配置
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #邮件发送
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.qq.com')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '269598358@qq.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'iupitmmafwvmbjha')
    #BOOTSTRAP 使用本地的静态文件
    BOOTSTRAP_SERVE_LOCAL = True
    #上传文件
    MAX_CONTENT_LENGTH = 1024*1024*8
    UPLOADED_PHOTOS_DEST = os.path.join(base_dir,'static/upload')

    #完成特定环境的初始化
    @staticmethod
    def init_app():
        pass

## 开发环境配置
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(base_dir,'static/db/blog-dev.sqlite')
#测试环境配置
class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(base_dir,'static/db/blog-test.sqlite')

#生产环境配置
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(base_dir,'static/db/blog.sqlite')

config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,
    #默认环境
    'default':DevelopmentConfig
}