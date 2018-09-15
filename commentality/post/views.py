from flask import request, g, Blueprint, json, Response
from commentality.authentication import Auth
from commentality.post.models import Post
from commentality.post.serializers import post_schema

blueprint = Blueprint('post', __name__)

@blueprint.route('/', methods=['POST'])
@Auth.auth_required
def create():
  req_data = request.get_json()
  req_data['owner_id'] = g.user.get('id')
  data, error = post_schema.load(req_data)
  if error:
    return custom_response(error, 400)
  post = Post(data)
  post.save()
  data = post_schema.dump(post).data
  return custom_response(data, 201)

@blueprint.route('/', methods=['GET'])
def get_all():
  posts = Post.get_all_blogposts()
  data = post_schema.dump(posts, many=True).data
  return custom_response(data, 200)

@blueprint.route('/<int:post_id>', methods=['GET'])
def get_one(post_id):
  post = Post.get_one_blogpost(post_id)
  if not post:
    return custom_response({'error': 'post not found'}, 404)
  data = post_schema.dump(post).data
  return custom_response(data, 200)

@blueprint.route('/<int:post_id>', methods=['PUT'])
@Auth.auth_required
def update(post_id):
  req_data = request.get_json()
  post = Post.get_one_blogpost(post_id)
  if not post:
    return custom_response({'error': 'post not found'}, 404)
  data = post_schema.dump(post).data
  if data.get('owner_id') != g.user.get('id'):
    return custom_response({'error': 'permission denied'}, 400)

  data, error = post_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 400)
  post.update(data)

  data = post_schema.dump(post).data
  return custom_response(data, 200)

@blueprint.route('/<int:post_id>', methods=['DELETE'])
@Auth.auth_required
def delete(post_id):
  post = Post.get_one_blogpost(post_id)
  if not post:
    return custom_response({'error': 'post not found'}, 404)
  data = post_schema.dump(post).data
  if data.get('owner_id') != g.user.get('id'):
    return custom_response({'error': 'permission denied'}, 400)

  post.delete()
  return custom_response({'message': 'deleted'}, 204)


def custom_response(res, status_code):
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )

