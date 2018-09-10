from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import app_config

def create_app(env_name):
  app = Flask(__name__)
  app.config.from_object(app_config[env_name])

  db = SQLAlchemy(app)
  bcrypt = Bcrypt(app)
  migrate = Migrate(app, db)

  @app.route('/', methods=['GET'])
  def index():
    return 'Commentality!!!'

  return app

