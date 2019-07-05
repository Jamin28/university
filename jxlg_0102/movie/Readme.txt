说明：本次项目采用的sqlite3

运行csv_to_sqlite.py文件，可将数据导入db.sqlite，如果使用本项目已存在的则可以不需要重新导入

在终端使用python manager.py createsuperuser 可创建管理员 登陆可进行修改   http://127.0.0.1:8000/admin/

留言板处需要使用 pip install django-tinymce

验证码需要  pip install django-simple-captcha

登录时密码进行了加密，数据库中无法看到，用户meijiaming的密码是123456789

由装饰器，加在需要的函数前面，则该视图函数在未登录时都会跳转到登录页面