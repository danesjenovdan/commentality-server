from neomodel import (StructuredNode, StringProperty, RelationshipTo,
  RelationshipFrom, UniqueIdProperty, DateTimeProperty, One)
from vote import VoteRelationship

class Comment(StructuredNode):
  uid = UniqueIdProperty()
  created_at = DateTimeProperty(default_now=True)
  modified_at = DateTimeProperty(default_now=True)

  contents = StringProperty(required=True)
  owner = RelationshipTo('user.models.User', 'OWNED_BY', cardinality=One)
  article = RelationshipTo('article.models.Article', 'POSTED_ON', cardinality=One)
  voters = RelationshipFrom('user.models.User', 'VOTED_FOR', model=VoteRelationship)

  @staticmethod
  def get_all():
    return Comment.nodes

  @staticmethod
  def get(uid):
    return Comment.nodes.get_or_none(uid=uid)

  def __repr__(self):
    return '<Comment {}>'.format(self.uid)
