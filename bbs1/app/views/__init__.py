from .main import main
from .users import users
from .posts import posts

DEFAULT_BLUEPRINT = (
    (main,''),
    (users,'/users'),
    (posts,'/posts')
)


def config_blueprint(app):
    for blueprint,url_prefix in DEFAULT_BLUEPRINT:
       app.register_blueprint(blueprint,url_prefix=url_prefix)