from flask import request, Blueprint, g
from authentication import Auth
from common import custom_response
from media_property.models import MediaProperty
from media_property.serializers import media_peroperty_schema

from user import otp

# logging
import app

#  encryption
from config import app_config
import hmac
import hashlib

blueprint = Blueprint('user', __name__)