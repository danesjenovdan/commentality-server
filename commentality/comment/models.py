from neomodel import (StructuredNode, StringProperty, DateTimeProperty,
    UniqueIdProperty, RelationshipFrom)

class Comment(StructuredNode):
  uid = UniqueIdProperty()
  contents = StringProperty(required=True)
  created_at = DateTimeProperty(default_now=True)
  modified_at = DateTimeProperty(default_now=True)

  owner = RelationshipFrom('commentality.comment.models.User', 'OWNS')

  def __init__(self, data):
    self.contents = data.get('contents')
    self.owner = data.get('owner')

  @staticmethod
  def get_all_comments():
    return Comment.nodes

  @staticmethod
  def get_one_comment(uid):
    return Comment.nodes.get_or_none(uid=uid)

  def __repr__(self):
    return '<Comment {}>'.format(self.id)
