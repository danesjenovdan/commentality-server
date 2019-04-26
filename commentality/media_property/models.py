from neomodel import (StructuredNode, StringProperty,
  RelationshipFrom, UniqueIdProperty, DateTimeProperty, RelationshipTo)

from config import app_config
import hashlib
import app

from common import CommentalityModel

class MediaProperty(CommentalityModel):
  name = StringProperty()
  articles = RelationshipFrom('article.models.Article', 'OWNED_BY')
  editors = RelationshipTo('user.models.User', 'EDITED_BY')
  banned_users = RelationshipFrom('user.models.User', 'BANNED_ON')
