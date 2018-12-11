from neomodel import (StringProperty, EmailProperty, RelationshipFrom)

from commentality.extensions import bcrypt
from commentality.base import BaseModel


class User(BaseModel):
  name = StringProperty(required=True)
  email = EmailProperty(required=True, unique_index=True)
  password = StringProperty()
  comments = RelationshipFrom('commentality.comment.models.Comment', 'OWNED_BY')

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
