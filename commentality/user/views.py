from flask import request, json, Response, Blueprint, g
from commentality.authentication import Auth
from .models import User
from .serializers import user_schema

blueprint = Blueprint('user', __name__)

@blueprint.route('/', methods=['POST'])
def create():
  req_data = request.get_json()
  data, error = user_schema.load(req_data)

  if error:
    return custom_response(error, 400)

  user_in_db = User.get_by_email(data.get('email'))
  if user_in_db:
    message = {'error': 'User already exists'}
    return custom_response(message, 400)

  user = User(
    name=data.get('name'),
    email=data.get('email'),
  )

  user.set_password(password=data.get('password'))
  user.save()
  serialized_data = user_schema.dump(user).data
  token = Auth.generate_token(serialized_data.get('uid'))
  return custom_response({'jwt_token': token}, 201)

@blueprint.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
  users = User.get_all()
  serialized_users = user_schema.dump(users, many=True).data
  return custom_response(serialized_users, 200)

@blueprint.route('/<int:user_uid>', methods=['GET'])
@Auth.auth_required
def get(user_uid):
  user = User.get(user_uid)
  if not user:
    return custom_response({'error': 'user not found'}, 404)

  serialized_user = user_schema.dump(user).data
  return custom_response(serialized_user, 200)

@blueprint.route('/me', methods=['PUT'])
@Auth.auth_required
def update():
  req_data = request.get_json()
  data, error = user_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 400)

  user = User.get(g.user.get('uid'))
  user.update(data)
  serialized_user = user_schema.dump(user).data
  return custom_response(serialized_user, 200)

@blueprint.route('/me', methods=['DELETE'])
@Auth.auth_required
def delete():
  user = User.get(g.user.get('uid'))
  user.delete()
  return custom_response({'message': 'deleted'}, 204)

@blueprint.route('/me', methods=['GET'])
@Auth.auth_required
def get_me():
  user = User.get(g.user.get('uid'))
  serialized_user = user_schema.dump(user).data
  return custom_response(serialized_user, 200)


@blueprint.route('/login', methods=['POST'])
def login():
  req_data = request.get_json()

  data, error = user_schema.load(req_data, partial=True)
  if error:
    return custom_response(error, 400)
  if not data.get('email') or not data.get('password'):
    return custom_response({'error': 'you need email and password to sign in'}, 400)
  user = User.get_by_email(data.get('email'))
  if not user:
    return custom_response({'error': 'invalid credentials'}, 400)
  if not user.check_password(data.get('password')):
    return custom_response({'error': 'invalid credentials'}, 400)
  serialized_data = user_schema.dump(user).data
  token = Auth.generate_token(serialized_data.get('uid'))
  return custom_response({'jwt_token': token}, 200)


def custom_response(res, status_code):
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )
