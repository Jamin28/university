import os

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'ligong'
USERNAME = 'root'
PASSWORD = '123456'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

DEBUG = True

SECRET_KEY = os.urandom(24)

MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.qq.com')
MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '269598358@qq.com')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'iupitmmafwvmbjha')

base_dir = os.path.abspath(os.path.dirname(__file__))
MAX_CONTENT_LENGTH = 1024*1024*8
UPLOADED_PHOTOS_DEST = os.path.join(base_dir,'static/images')

BOOTSTRAP_SERVE_LOCAL = True
