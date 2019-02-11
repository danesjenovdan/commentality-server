from flask import request, g, Blueprint
from authentication import Auth
from common import custom_response
from comment.models import Comment
from user.models import User
from article.models import Article
from comment.serializers import comment_schema

blueprint = Blueprint('comment', __name__)

@blueprint.route('/', methods=['POST'])
@Auth.auth_required
def create():
  req_data = request.get_json()
  data, error = comment_schema.load(req_data)
  if error:
    return custom_response(error, 400)

  # Create and save comment
  comment = Comment(contents=data['contents'])
  comment.save()

  # Connect owner
  owner_id = g.user.get('uid')
  owner = User.get(owner_id)
  comment.owner.connect(owner)

  article_external_id = data['article_external_id']
  article = Article.get_by_external_id(article_external_id)
  if not article:
    article = Article(external_id=article_external_id)
    article.save()
  comment.article.connect(article)

  data = comment_schema.dump(comment).data
  return custom_response(data, 201)

@blueprint.route('/', methods=['GET'])
def get_all():
  comments = Comment.get_all()
  data = comment_schema.dump(comments, many=True).data
  return custom_response(data, 200)

@blueprint.route('/<comment_id>', methods=['GET'])
def get_one(comment_id):
  comment = Comment.get(comment_id)
  if not comment:
    return custom_response({'error': 'comment not found'}, 404)
  data = comment_schema.dump(comment).data
  return custom_response(data, 200)

@blueprint.route('/<comment_id>', methods=['PUT'])
@Auth.auth_required
def update(comment_id):
  req_data = request.get_json()
  comment = Comment.get(comment_id)
  if not comment:
    return custom_response({'error': 'comment not found'}, 404)
  data = comment_schema.dump(comment).data
  if data.get('owner_id') != g.user.get('uid'):
    return custom_response({'error': 'permission denied'}, 400)

  data, error = comment_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 400)
  comment.update(data)

  data = comment_schema.dump(comment).data
  return custom_response(data, 200)

@blueprint.route('/<comment_id>', methods=['DELETE'])
@Auth.auth_required
def delete(comment_id):
  comment = Comment.get(comment_id)
  if not comment:
    return custom_response({'error': 'comment not found'}, 404)
  data = comment_schema.dump(comment).data
  if data.get('owner_id') != g.user.get('uid'):
    return custom_response({'error': 'permission denied'}, 400)

  comment.delete()
  return custom_response({'message': 'deleted'}, 204)

@blueprint.route('/vote/<comment_id>', methods=['POST'])
@Auth.auth_required
def vote(comment_id):
  comment = Comment.get(comment_id)
  if not comment:
    return custom_response({'error': 'comment not found'}, 404)

  voter_id = g.user.get('uid')
  voter = User.get(voter_id)

  vote_type = request.get_json().get('type')
  valid_vote_types = ['like', 'dislike', 'meh']

  if not vote_type or vote_type not in valid_vote_types :
    return custom_response({'error': 'invalid vote'}, 404)

  existing_vote = comment.voters.relationship(voter)
  if existing_vote:
    # existing_vote.type = vote_type
    # existing_vote.save()
    return custom_response({'error': 'already voted'}, 404)
  else:
    comment.voters.connect(voter, {'type': vote_type})

  data = comment_schema.dump(comment).data
  return custom_response(data, 201)

