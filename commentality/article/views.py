from flask import Blueprint, json, Response, request, g
from common import custom_response
from authentication import Auth
from article.models import Article
from user.models import User
from article.serializers import article_schema, articles_schema

blueprint = Blueprint('article', __name__)

@blueprint.route('/<article_external_id>', methods=['GET'])
def get_one(article_external_id):
  article = Article.get_by_external_id(article_external_id)
  if not article:
    article = Article(external_id=article_external_id)
    article.save()

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