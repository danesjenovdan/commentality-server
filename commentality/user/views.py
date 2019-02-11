from flask import request, Blueprint, g
from authentication import Auth
from common import custom_response
from user.models import User
from user.serializers import user_schema

from user import otp

# logging
import app

blueprint = Blueprint('user', __name__)

@blueprint.route('/', methods=['POST'])
def get_code():
  '''
    Takes number and creates or logs user in.
  '''
  req_data = request.get_json()
  data, error = user_schema.load(req_data)

  if error:
    return custom_response(error, 400)

  if data['number']:
    app.app.logger.info('Got number: %s, sending verification code.' % data['number'])
    verification_code = otp.send_confirmation_code(data['number'])

    user_in_db = User.get_by_number(data['number'])
    if not user_in_db:
      user = User(
        number = data['number']
      )
      user.save()
    else:
      user = user_in_db
  
  user.code = verification_code
  user.save()
  
  return custom_response({
    'status': 'Sent verification code to %s' % data['number']
  }, 200)

@blueprint.route('/verify', methods=['POST'])
def verify():
  req_data = request.get_json()
  data, error = user_schema.load(req_data)

  if error:
    return custom_response(error, 400)

  user_by_code = User.get_by_code(str(req_data['code']))

  if user_by_code and user_by_code.number == str(req_data['number']):
    user = user_by_code

    # destroy code
    user.code = ''
    user.save()

    serialized_data = user_schema.dump(user).data
    token = Auth.generate_token(serialized_data.get('uid'))
    return custom_response({
      'jwt_token': token,
      'uid': serialized_data.get('uid'),
    }, 201)
  else:
    message = {'error': 'Wrong verification code.'}
    return custom_response(message, 400)

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
