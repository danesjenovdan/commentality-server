from flask import Blueprint, json, Response, request, g
from common import custom_response
from authentication import Auth
from article.models import Article
from user.models import User
from article.serializers import article_schema, articles_schema, authenthicated_article_schema

blueprint = Blueprint('article', __name__)

@blueprint.route('/<uid>', methods=['GET'])
def get_one(uid):
  article = Article.get(uid)
  if not article:
    return custom_response({'error': 'article not found'}, 404)

  token = request.headers.get('api-token')
  data = Auth.decode_token(token)
  print(data, data['data'].keys(), file=sys.stderr)
  if 'user_uid' in data['data'].keys():
    user_id = data['data']['user_uid']
    user = User.get(user_id)
  else:
    user = None
    
  if user:
    data = authenthicated_article_schema.dump(article).data
  else:
    data = article_schema.dump(article).data
  return custom_response(data, 200)


@blueprint.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
  owner_id = g.user.get('uid')
  owner = User.get(owner_id)
  articles = owner.articles.all()
  data = articles_schema.dump(articles).data
  return custom_response(data, 200)


@blueprint.route('/', methods=['POST'])
@Auth.auth_required
def create():
  req_data = request.get_json()
  data, error = article_schema.load(req_data)
  if error:
    return custom_response(error, 400)

  # Create and save article
  article = Article(
    external_id=data['external_id'],
    title = data['title']
  )
  article.save()

  # Connect owner
  owner_id = g.user.get('uid')
  owner = User.get(owner_id)
  article.owner.connect(owner)

  data = article_schema.dump(article).data
  return custom_response(data, 201)