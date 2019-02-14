from neomodel import (StructuredNode, StringProperty, RelationshipTo,
  RelationshipFrom, UniqueIdProperty, DateTimeProperty, One)
from relations.vote import VoteRelationship
from relations.comment import CommentRelationship

class Comment(StructuredNode):
  uid = UniqueIdProperty()
  created_at = DateTimeProperty(default_now=True)
  modified_at = DateTimeProperty(default_now=True)

  contents = StringProperty(required=True)
  owner = RelationshipTo('user.models.User', 'OWNED_BY', cardinality=One, model=CommentRelationship)
  article = RelationshipTo('article.models.Article', 'POSTED_ON')#, cardinality=One)
  voters = RelationshipFrom('user.models.User', 'VOTED_FOR', model=VoteRelationship)
  hidden = RelationshipTo('article.models.Article', 'HIDDEN_ON')

  @staticmethod
  def get_all():
    return Comment.nodes

  @staticmethod
  def get(uid):
    return Comment.nodes.get_or_none(uid=uid)

  def __repr__(self):
    return '<Comment {}>'.format(self.uid)

  def update(self, data):
    for name, value in data.items():
      setattr(self, name, value)
    self.save()
