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
  editors = RelationshipTo('user.models.User', 'EDITED_BY')
  banned_users = RelationshipFrom('user.models.User', 'BANNED_ON')

  @staticmethod
  def get_all():
    return MediaProperty.nodes

  @staticmethod
  def get(uid):
    return MediaProperty.nodes.get_or_none(uid=uid)

  def __repr__(self):
    return '<MediaProperty({name!r})>'.format(name=self.name)