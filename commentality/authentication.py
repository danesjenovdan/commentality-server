import jwt
import os
import datetime
from flask import json, Response, request, g
from functools import wraps
from user.models import User


class Auth():
  """
  Auth Class
  """
  @staticmethod
  def generate_token(user_uid):
    """
    Generate Token Method
    """
    try:
      payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
        'sub': user_uid
      }
      return jwt.encode(
        payload,
        os.getenv('JWT_SECRET_KEY'),
        'HS256'
      ).decode("utf-8")
    except Exception as e:
      return Response(
        mimetype="application/json",
        response=json.dumps({'error': 'error in generating user token'}),
        status=500
      )

  @staticmethod
  def generate_long_term_token(user_uid):
    """
    Generate Token Method
    """
    try:
      payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365),
        'iat': datetime.datetime.utcnow(),
        'sub': user_uid
      }
      return jwt.encode(
        payload,
        os.getenv('JWT_SECRET_KEY'),
        'HS256'
      ).decode("utf-8")
    except Exception as e:
      return Response(
        mimetype="application/json",
        response=json.dumps({'error': 'error in generating user token'}),
        status=500
      )

  @staticmethod
  def decode_token(token):
    """
    Decode token method
    """
    re = {'data': {}, 'error': {}}
    try:
      payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'))
      re['data'] = {'user_uid': payload['sub']}
    except jwt.ExpiredSignatureError as e1:
      re['error'] = {'message': 'token expired, please login again'}
    except jwt.InvalidTokenError:
      re['error'] = {'message': 'Invalid token, please try again with a new token'}

    return re

  # decorator
  @staticmethod
  def auth_required(func):
    """
    Auth decorator
    """
    @wraps(func)
    def decorated_auth(*args, **kwargs):
      if 'api-token' not in request.headers:
        return Response(
          mimetype="application/json",
          response=json.dumps({'error': 'Authentication token is not available, please login to get one'}),
          status=401
        )
      token = request.headers.get('api-token')
      data = Auth.decode_token(token)
      if data['error']:
        return Response(
          mimetype="application/json",
          response=json.dumps(data['error']),
          status=401
        )

      user_uid = data['data']['user_uid']
      check_user = User.get(user_uid)
      if not check_user:
        return Response(
          mimetype="application/json",
          response=json.dumps({'error': 'user does not exist, invalid token'}),
          status=401
        )
      g.user = {'uid': user_uid}
      return func(*args, **kwargs)
    return decorated_auth

  # decorator
  @staticmethod
  def superuser_required(func):
    """
    Superuser decorator
    """
    @wraps(func)
    def decorated_auth(*args, **kwargs):
      if 'api-token' not in request.headers:
        return Response(
          mimetype="application/json",
          response=json.dumps({'error': 'Authentication token is not available, please login to get one'}),
          status=401
        )
      token = request.headers.get('api-token')
      data = Auth.decode_token(token)
      if data['error']:
        return Response(
          mimetype="application/json",
          response=json.dumps(data['error']),
          status=401
        )

      user_uid = data['data']['user_uid']
      check_user = User.get(user_uid)
      if not check_user or not check_user.is_superuser:
        return Response(
          mimetype="application/json",
          response=json.dumps({'error': 'user does not exist, invalid token'}),
          status=401
        )
      g.user = {'uid': user_uid}
      return func(*args, **kwargs)
    return decorated_auth
