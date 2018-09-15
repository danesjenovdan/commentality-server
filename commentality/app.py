from flask import Flask
from commentality.extensions import db, bcrypt, migrate, cors

from commentality.config import app_config
from commentality import user, post

def create_app(env_name):
  app = Flask(__name__)
  app.config.from_object(app_config[env_name])

  register_extensions(app)
  register_blueprints(app)

  @app.route('/', methods=['GET'])
  def index():
    return 'Commentality!!!'

  return app

def register_extensions(app):
  db.init_app(app)
  bcrypt.init_app(app)
  migrate.init_app(app, db)

def register_blueprints(app):
  db.init_app(app)
  bcrypt.init_app(app)
  migrate.init_app(app, db)
  app.register_blueprint(user.views.blueprint, url_prefix='/api/v1/users')
  app.register_blueprint(post.views.blueprint, url_prefix='/api/v1/posts')
