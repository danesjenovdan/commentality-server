from flask import request, Blueprint, g
from authentication import Auth
from common import custom_response
from media_property.models import MediaProperty
from media_property.serializers import media_peroperty_schema
from user.models import User

# logging
import app

#  encryption
from config import app_config
import hmac
import hashlib

blueprint = Blueprint('property', __name__)


@blueprint.route('/', methods=['POST'])
@Auth.superuser_required
def create():
  req_data = request.get_json()
  data, error = media_peroperty_schema.load(req_data)
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
  
  # TODO: add editors with separate endpoint
  media_property.editors.connect(owner)

  data = media_peroperty_schema.dump(media_property).data
  return custom_response(data, 201)