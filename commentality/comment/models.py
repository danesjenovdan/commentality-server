from neomodel import (StructuredNode, StringProperty, DateTimeProperty,
    UniqueIdProperty, RelationshipTo, One)

class Comment(StructuredNode):
  uid = UniqueIdProperty()
  contents = StringProperty(required=True)
  created_at = DateTimeProperty(default_now=True)
  modified_at = DateTimeProperty(default_now=True)

  owner = RelationshipTo('commentality.user.models.User', 'OWNED_BY', cardinality=One)

  @staticmethod
  def get_all():
    return Comment.nodes

  @staticmethod
  def get_one_comment(uid):
    return Comment.nodes.get_or_none(uid=uid)

  def __repr__(self):
    return '<Comment {}>'.format(self.uid)
