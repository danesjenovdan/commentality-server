from flask import request, Blueprint, g
from authentication import Auth
from common import custom_response
from media_property.models import MediaProperty
from media_property.serializers import media_property_schema, media_properties_schema, most_discussed_schema
from user.models import User

# logging
import app

#  encryption
from config import app_config
import hmac
import hashlib

blueprint = Blueprint('property', __name__)

@blueprint.route('/', methods=['GET'])
@Auth.superuser_required
def all():
  properties = media_properties_schema.dump(MediaProperty.get_all())

  return custom_response(properties, 200)

@blueprint.route('/', methods=['POST'])
@Auth.superuser_required
def create():
  req_data = request.get_json()
  data, error = media_property_schema.load(req_data)
  if error:
    return custom_response(error, 400)

  # Create and save property
  media_property = MediaProperty(
    name = data['name'],
  )
  media_property.save()

  # Connect owner
  owner_id = g.user.get('uid')
  owner = User.get(owner_id)
  
  media_property.editors.connect(owner)

  data = media_property_schema.dump(media_property).data
  return custom_response(data, 201)

@blueprint.route('/add_editor/<editor_uid>', methods=['POST'])
@Auth.superuser_required
def add_editor(editor_uid):
  # get media property
  req_data = request.get_json()
  data, error = media_property_schema.load(req_data)
  if error:
    return custom_response(error, 400)

  editor = User.get(editor_uid)
  media_property = MediaProperty.get(data['uid'])

  media_property.editors.connect(editor)

  data = media_property_schema.dump(media_property).data
  return custom_response(data, 200)

@blueprint.route('/most_discussed/<property_uid>', methods=['GET'])
def most_discussed(property_uid):
  data = most_discussed_schema.dump(MediaProperty.get(uid=property_uid)).data

  return custom_response(data, 200)