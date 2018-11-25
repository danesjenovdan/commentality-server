from commentality.extensions import bcrypt
from neomodel import (StructuredNode, StringProperty, DateTimeProperty,
    UniqueIdProperty, RelationshipTo, EmailProperty)

class User(StructuredNode):
  uid = UniqueIdProperty()
  name = StringProperty(required=True)
  email = EmailProperty(required=True, unique_index=True)
  password = StringProperty()
  created_at = DateTimeProperty(default_now=True)
  modified_at = DateTimeProperty(default_now=True)

  comments = RelationshipTo('commentality.comment.models.Comment', 'OWNS')

  def __init__(self, name, email, **kwargs):
    StructuredNode.__init__(self, name=name, email=email, **kwargs)

  def set_password(self, password):
    self.password = bcrypt.generate_password_hash(password).decode('utf-8')

  def check_password(self, value):
    check = bcrypt.check_password_hash(self.password, value)
    print('check is: {})'.format(check))
    # print('check is: {} ({}, {})'.format(check, self.password, value))
    return check

  def __repr__(self):
    return '<User({name!r})>'.format(name=self.name)

  @staticmethod
  def get_all_users():
    return User.nodes

  @staticmethod
  def get_one_user(uid):
    return User.nodes.get_or_none(uid=uid)

  @staticmethod
  def get_user_by_email(email):
    return User.nodes.get_or_none(email=email)
