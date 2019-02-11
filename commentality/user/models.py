from neomodel import (StructuredNode, IntegerProperty,
  RelationshipFrom, UniqueIdProperty, DateTimeProperty, RelationshipTo)

from extensions import bcrypt

from vote import VoteRelationship

class User(StructuredNode):
  uid = UniqueIdProperty()
  created_at = DateTimeProperty(default_now=True)
  modified_at = DateTimeProperty(default_now=True)

  number = IntegerProperty()
  comments = RelationshipFrom('comment.models.Comment', 'OWNED_BY')
  votes = RelationshipTo('comment.models.Comment', 'VOTED_FOR', model=VoteRelationship)

  @staticmethod
  def get_all():
    return User.nodes

  @staticmethod
  def get(uid):
    return User.nodes.get_or_none(uid=uid)

  def __repr__(self):
    return '<User({uid!r})>'.format(uid=self.uid)
