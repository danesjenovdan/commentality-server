import neomodel
from flask import Flask

from extensions import bcrypt, cors, init_db
from config import app_config
import user
import article
import comment
import media_property


def register_extensions(app):
  init_db(app)
  bcrypt.init_app(app)
  cors.init_app(app)

def register_blueprints(app):
  app.register_blueprint(article.views.blueprint, url_prefix='/backend/api/v2/articles')
  app.register_blueprint(comment.views.blueprint, url_prefix='/backend/api/v2/comments')
  app.register_blueprint(user.views.blueprint, url_prefix='/backend/api/v2/users')
  app.register_blueprint(media_property.views.blueprint, url_prefix='/backend/api/v2/properties')

app = Flask(__name__)

app.secret_key = 'my secret key' # TODO
app.config.from_object(app_config['development'])

register_extensions(app)
register_blueprints(app)

@app.route('/backend/', methods=['GET'])
def index():
  return 'Commentality!!!'
