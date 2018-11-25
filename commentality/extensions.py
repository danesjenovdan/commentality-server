from flask_bcrypt import Bcrypt
from flask_cors import CORS
from neomodel import config

bcrypt = Bcrypt()
cors = CORS()

def init_db(app):
  config.AUTO_INSTALL_LABELS = app.config['DEBUG']
  config.DATABASE_URL = app.config['DATABASE_URL']
