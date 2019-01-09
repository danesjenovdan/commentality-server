from neomodel import (StructuredNode, StringProperty, EmailProperty,
  RelationshipFrom, UniqueIdProperty, DateTimeProperty, RelationshipTo)

from extensions import bcrypt

from vote import VoteRelationship

class User(StructuredNode):
  uid = UniqueIdProperty()
  created_at = DateTimeProperty(default_now=True)
  modified_at = DateTimeProperty(default_now=True)

  name = StringProperty(required=True)
  email = EmailProperty(required=True, unique_index=True)
  password = StringProperty()
  comments = RelationshipFrom('comment.models.Comment', 'OWNED_BY')
  votes = RelationshipTo('comment.models.Comment', 'VOTED_FOR', model=VoteRelationship)

  @staticmethod
  def get_all():
    return User.nodes

  @staticmethod
  def get(uid):
    return User.nodes.get_or_none(uid=uid)

  def set_password(self, password):
    self.password = bcrypt.generate_password_hash(password).decode('utf-8')

  def check_password(self, value):
    check = bcrypt.check_password_hash(self.password, value)
    return check

  def __repr__(self):
    return '<User({name!r})>'.format(name=self.name)

  @staticmethod
  def get_by_email(email):
    return User.nodes.get_or_none(email=email)
