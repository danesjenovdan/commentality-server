from flask import Blueprint, json, Response, request, g
from common import custom_response
from authentication import Auth
from article.models import Article
from user.models import User
from article.serializers import article_schema, articles_schema, authenthicated_article_schema

import app

blueprint = Blueprint('article', __name__)

@blueprint.route('/<uid>', methods=['GET'])
def get_one(uid):
  article = Article.get(uid)
  if not article:
    return custom_response({'error': 'article not found'}, 404)

  token = request.headers.get('api-token')
  data = Auth.decode_token(token)
  if 'user_uid' in data['data'].keys():
    user_id = data['data']['user_uid']
    user = User.get(user_id)
  else:
    user = None
    
  if user:
    data = authenthicated_article_schema.dump(article).data
    # get voted comments
    results, columns = article.cypher('MATCH (a:Article)<-[:POSTED_ON]-(c)<-[r:VOTED_FOR]-(u:User) WHERE u.uid = "' + user_id + '" AND a.uid = "' + article.uid + '" RETURN c')
    data['voted'] = [article.inflate(row[0]).uid for row in results]
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


@blueprint.route('/<uid>', methods=['PUT'])
def patch(uid):
  article = Article.get(uid)
  if not article:
    return custom_response({'error': 'article not found'}, 404)

  req_data = request.get_json()
  data, error = article_schema.load(req_data)
  if error:
    return custom_response(error, 400)

  if data.get('owner_id') != g.user.get('uid'):
    return custom_response({'error': 'permission denied'}, 400)

  article.update(data)

  data = article_schema.dump(article).data
  return custom_response(data, 200)