from neomodel import (StructuredNode, StringProperty,
  RelationshipFrom, UniqueIdProperty, DateTimeProperty, RelationshipTo)

from config import app_config
import hashlib
import app


class MediaProperty(StructuredNode):
  uid = UniqueIdProperty()
  created_at = DateTimeProperty(default_now=True)
  modified_at = DateTimeProperty(default_now=True)

  name = StringProperty()
  articles = RelationshipFrom('article.models.Article', 'OWNED_BY')