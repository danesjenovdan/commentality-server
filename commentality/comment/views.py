from flask import request, g, Blueprint
from authentication import Auth
from common import custom_response
from comment.models import Comment
from user.models import User
from article.models import Article
from comment.serializers import comment_schema

import app

blueprint = Blueprint('comment', __name__)


@blueprint.route('/', methods=['POST'])
@Auth.auth_required
def create():
  req_data = request.get_json()
  data, error = comment_schema.load(req_data)
  if error:
    return custom_response(error, 400)

  article_uid = data['article_uid']
  article = Article.get(article_uid)
  if not article:
    return custom_response({'error': 'Article does not exists.'}, 404)

  if not article.can_comment:
    return custom_response({'error': 'commenting locked'}, 400)

  user_id = g.user.get('uid')
  user = User.get(user_id)

  if not user:
    return custom_response({'error': 'Only registered users can comment.'}, 400)

  rel = article.owner.single().banned_users.relationship(user)
  if rel:
    return custom_response({'error': 'you are banned on this property.'}, 400)

  is_editor = article.owner.single().editors.is_connected(user)

  # check if the user has already commented
  my_comments = article.cypher(
    'MATCH (a:Article) <-- (c:Comment) -[:OWNED_BY]-> (u:User) '
    'WHERE a.uid = "'+ article.uid + '" '
    'AND u.uid="' + user.uid +'" '
    'RETURN COUNT(c)'
  )[0][0][0]

  if not is_editor:
    if my_comments:
      return custom_response({'error': 'You have already commented on this article.'}, 400)

  # check if user voted for all comments of article
  total_comments = len(article.comments)
  voted_comments = article.cypher(
    'MATCH (a:Article) <-- (c:Comment) <-[:VOTED_FOR]- (u:User)'
    'WHERE a.uid = "' + article.uid + '" '
    'AND u.uid="'+ user.uid + '" '
    'RETURN COUNT(c)'
  )[0][0][0]

  if is_editor or total_comments == voted_comments:
    # Create and save comment
    comment = Comment(contents=data['contents'])
    comment.save()

    comment.article.connect(article)

    # Connect owner
    comment.owner.connect(user)

    data = comment_schema.dump(comment).data
    return custom_response(data, 201)
  else:
    return custom_response({'error': 'first, vote for all comments'}, 400)


@blueprint.route('/', methods=['GET'])
@Auth.superuser_required
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
  owner_id = g.user.get('uid')
  owner = User.get(owner_id)

  is_editor = comment.article.single().owner.single().editors.is_connected(owner)
  if not is_editor:
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
  owner_id = g.user.get('uid')
  owner = User.get(owner_id)
  article = comment.article.single()
  is_editor = article.owner.single().editors.is_connected(owner)

  if not is_editor:
    return custom_response({'error': 'permission denied'}, 400)
  
  comment.hidden.connect(article)
  comment.article.disconnect(article)

  return custom_response({'message': 'hidden'}, 204)


@blueprint.route('/vote/<comment_id>', methods=['POST'])
@Auth.auth_required
def vote(comment_id):
  comment = Comment.get(comment_id)
  if not comment:
    return custom_response({'error': 'comment not found'}, 404)

  if not comment.article.single().can_vote:
    return custom_response({'error': 'voting locked'}, 400)

  voter_id = g.user.get('uid')
  voter = User.get(voter_id)

  rel = comment.article.single().owner.single().banned_users.relationship(voter)
  if rel:
    return custom_response({'error': 'you are banned on this property.'}, 400)

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

