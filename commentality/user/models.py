from neomodel import (StructuredNode, StringProperty,
  RelationshipFrom, UniqueIdProperty, DateTimeProperty, RelationshipTo,
  BooleanProperty)

from config import app_config
import hashlib
import app

from vote import VoteRelationship

class User(StructuredNode):
  uid = UniqueIdProperty()
  created_at = DateTimeProperty(default_now=True)
  modified_at = DateTimeProperty(default_now=True)

  number = StringProperty()
  code = StringProperty()
  is_superuser = BooleanProperty(default=False)
  comments = RelationshipFrom('comment.models.Comment', 'OWNED_BY')
  votes = RelationshipTo('comment.models.Comment', 'VOTED_FOR', model=VoteRelationship)
  articles = RelationshipFrom('article.models.Article', 'OWNED_BY')

  @staticmethod
  def get_all():
    return User.nodes

  @staticmethod
  def get(uid):
    return User.nodes.get_or_none(uid=uid)
  
  @staticmethod
  def get_by_number(number):
    # TODO stop hardcoding development
    number_hash = hashlib.scrypt(password=str(number).encode('utf-8'), salt=app_config['development'].SECRET_KEY.encode('utf-8'), n=16384, r=8, p=8).hex()
    app.app.logger.info('I am get_by_number, this is my hash:\n%s\n\n' % str(number_hash))
    return User.nodes.get_or_none(number=number_hash)
  
  @staticmethod
  def get_by_code(code):
    return User.nodes.get_or_none(code=code)
  
  def set_number(self, number):
    # TODO stop hardcoding development
    number_hash = hashlib.scrypt(password=str(number).encode('utf-8'), salt=app_config['development'].SECRET_KEY.encode('utf-8'), n=16384, r=8, p=8).hex()
    self.number = number_hash

  # currently unused
  def check_number(self, number):
    # TODO stop hardcoding development
    number_hash = hashlib.scrypt(password=str(number).encode('utf-8'), salt=app_config['development'].SECRET_KEY.encode('utf-8'), n=16384, r=8, p=8).hex()
    app.app.logger.info('I am check_number, this is my hash:\n%s\n\n' % str(number_hash))
    return number_hash == self.number

  def __repr__(self):
    return '<User({uid!r})>'.format(uid=self.uid)
