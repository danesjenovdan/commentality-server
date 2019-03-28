import neomodel
from flask import Flask

from extensions import bcrypt, cors, init_db
from config import app_config
import user
import article
import comment

def create_app(env_name):
  app = Flask(__name__)
  app.config.from_object(app_config[env_name])

  register_extensions(app)
  register_blueprints(app)

  @app.route('/backend/', methods=['GET'])
  def index():
    return 'Commentality!!!'

  return app

def register_extensions(app):
  init_db(app)
  bcrypt.init_app(app)
  cors.init_app(app)

def register_blueprints(app):
  app.register_blueprint(article.views.blueprint, url_prefix='/backend/api/v1/articles')
  app.register_blueprint(comment.views.blueprint, url_prefix='/backend/api/v1/comments')
  app.register_blueprint(user.views.blueprint, url_prefix='/backend/api/v1/users')
