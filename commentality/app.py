import neomodel
from flask import Flask

from commentality.extensions import bcrypt, cors, init_db
from commentality.config import app_config
from commentality import user, comment

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
  init_db(app)
  bcrypt.init_app(app)
  cors.init_app(app)

def register_blueprints(app):
  app.register_blueprint(user.views.blueprint, url_prefix='/api/v1/users')
  app.register_blueprint(comment.views.blueprint, url_prefix='/api/v1/comments')
