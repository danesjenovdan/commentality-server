from flask import request, g, Blueprint, json, Response
from commentality.authentication import Auth
from .models import Comment
from .serializers import comment_schema

blueprint = Blueprint('comment', __name__)

@blueprint.route('/', methods=['POST'])
@Auth.auth_required
def create():
  req_data = request.get_json()
  req_data['owner_id'] = g.user.get('id')
  data, error = comment_schema.load(req_data)
  if error:
    return custom_response(error, 400)
  comment = comment(data)
  comment.save()
  data = comment_schema.dump(comment).data
  return custom_response(data, 201)

@blueprint.route('/', methods=['GET'])
def get_all():
  comments = comment.get_all_blogcomments()
  data = comment_schema.dump(comments, many=True).data
  return custom_response(data, 200)

@blueprint.route('/<int:comment_id>', methods=['GET'])
def get_one(comment_id):
  comment = comment.get_one_blogcomment(comment_id)
  if not comment:
    return custom_response({'error': 'comment not found'}, 404)
  data = comment_schema.dump(comment).data
  return custom_response(data, 200)

@blueprint.route('/<int:comment_id>', methods=['PUT'])
@Auth.auth_required
def update(comment_id):
  req_data = request.get_json()
  comment = comment.get_one_blogcomment(comment_id)
  if not comment:
    return custom_response({'error': 'comment not found'}, 404)
  data = comment_schema.dump(comment).data
  if data.get('owner_id') != g.user.get('id'):
    return custom_response({'error': 'permission denied'}, 400)

  data, error = comment_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 400)
  comment.update(data)

  data = comment_schema.dump(comment).data
  return custom_response(data, 200)

@blueprint.route('/<int:comment_id>', methods=['DELETE'])
@Auth.auth_required
def delete(comment_id):
  comment = comment.get_one_blogcomment(comment_id)
  if not comment:
    return custom_response({'error': 'comment not found'}, 404)
  data = comment_schema.dump(comment).data
  if data.get('owner_id') != g.user.get('id'):
    return custom_response({'error': 'permission denied'}, 400)

  comment.delete()
  return custom_response({'message': 'deleted'}, 204)


def custom_response(res, status_code):
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )

