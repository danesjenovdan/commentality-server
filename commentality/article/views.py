from flask import Blueprint, json, Response, request, g
from common import custom_response
from authentication import Auth
from article.models import Article
from user.models import User
from media_property.models import MediaProperty
from article.serializers import article_schema, articles_schema

import app

blueprint = Blueprint('article', __name__)

@blueprint.route('/<uid>', methods=['GET'])
def get_one(uid):
  article = Article.get(uid)
  if not article:
    return custom_response({'error': 'article not found'}, 404)

  # this could be made into an auth decorator (e.g. @Auth.auth_possible)
  token = request.headers.get('api-token')
  data = Auth.decode_token(token)
  if 'user_uid' in data['data'].keys():
    user_id = data['data']['user_uid']
    user = User.get(user_id)
  else:
    user = None

  comments_voted_on = []

  for comment in article.visible_comments:
    if user and comment.voters.is_connected(user):
      comments_voted_on.append(comment.uid)

  article.comments_voted_on = comments_voted_on

  data = article_schema.dump(article).data
  return custom_response(data, 200)


@blueprint.route('/', methods=['GET'])
@Auth.superuser_required
def get_all():
  articles =  Article.nodes.all()
  data = articles_schema.dump(articles).data
  return custom_response(data, 200)


@blueprint.route('/by_property/<property_uid>', methods=['GET'])
@Auth.auth_required
def get_all_by_property(property_uid):
  user_id = g.user.get('uid')
  user = User.get(user_id)
  media_property = MediaProperty.get(property_uid)
  if not media_property:
    return custom_response({'error': 'property not found'}, 404)
  if not media_property.editors.relationship(user):
    return custom_response({'error': 'permission denied'}, 400)
  articles =  media_property.articles
  data = articles_schema.dump(articles).data
  return custom_response(data, 200)


@blueprint.route('/', methods=['POST'])
@Auth.auth_required
def create():
  req_data = request.get_json()
  data, error = article_schema.load(req_data)
  if error:
    return custom_response(error, 400)

  media_property = MediaProperty.get(data['owner'])
  if not media_property:
    return custom_response({'error': 'property not found'}, 404)
  # Create and save article
  article = Article(
    external_id=data['external_id'],
    title = data['title']
  )
  article.save()
  article.owner.connect(media_property)

  data = article_schema.dump(article).data
  return custom_response(data, 201)


@blueprint.route('/<uid>', methods=['PATCH'])
@Auth.auth_required
def patch(uid):
  article = Article.get(uid)
  if not article:
    return custom_response({'error': 'article not found'}, 404)

  req_data = request.get_json()
  data, error = article_schema.load(req_data)
  if error:
    return custom_response(error, 400)

  user_id = g.user.get('uid')
  app.app.logger.info(user_id)
  user = User.get(user_id)

  if not article.owner.all()[0].editors.is_connected(user):
    return custom_response({'error': 'permission denied'}, 400)

  data['uid'] = uid
  data['id'] = article.id
  article.update(data)

  data = article_schema.dump(article).data
  return custom_response(data, 200)


@blueprint.route('/<uid>', methods=['DELETE'])
@Auth.auth_required
def delete(uid):
  article = Article.get(uid)
  if not article:
    return custom_response({'error': 'article not found'}, 404)

  user_id = g.user.get('uid')
  app.app.logger.info(user_id)
  user = User.get(user_id)

  if not article.owner.all()[0].editors.is_connected(user):
    return custom_response({'error': 'permission denied'}, 400)

  article.delete()
  return custom_response({'message': 'deleted'}, 204)
