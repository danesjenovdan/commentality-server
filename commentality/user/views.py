from flask import request, Blueprint, g, session
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
    session['number'] = data['number']
    session['verification_code'] = verification_code
  
  return custom_response({
    'status': 'Sent verification code to %s' % data['number']
  }, 200)

@blueprint.route('/verify', methods=['POST'])
def verify():
  req_data = request.get_json()
  data, error = user_schema.load(req_data)

  if error:
    return custom_response(error, 400)

  if session['verification_code'] == req_data['code']:
    user_in_db = User.get_by_number(session['number'])

    if not user_in_db:
      user = User(
        number = session['number']
      )
      user.save()
    else:
      user = user_in_db

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
