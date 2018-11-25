from neomodel import (StructuredNode, StringProperty, DateTimeProperty,
    UniqueIdProperty, RelationshipFrom, One)
from commentality.user.models import User

class Comment(StructuredNode):
  uid = UniqueIdProperty()
  contents = StringProperty(required=True)
  created_at = DateTimeProperty(default_now=True)
  modified_at = DateTimeProperty(default_now=True)

  owner = RelationshipFrom('commentality.comment.models.User', 'OWNS',
                           cardinality=One)

  @staticmethod
  def get_all():
    return Comment.nodes

  @staticmethod
  def get_one_comment(uid):
    return Comment.nodes.get_or_none(uid=uid)

  def __repr__(self):
    return '<Comment {}>'.format(self.uid)
