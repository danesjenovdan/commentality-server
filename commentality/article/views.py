from flask import Blueprint, json, Response
from common import custom_response
from article.models import Article
from article.serializers import article_schema

blueprint = Blueprint('article', __name__)

@blueprint.route('/<article_external_id>', methods=['GET'])
def get_one(article_external_id):
  article = Article.get_by_external_id(article_external_id)
  if not article:
    article = Article(external_id=article_external_id)
    article.save()

  data = article_schema.dump(article).data
  return custom_response(data, 200)
