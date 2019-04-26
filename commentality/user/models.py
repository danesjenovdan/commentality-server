from neomodel import (StructuredNode, StringProperty,
  RelationshipFrom, UniqueIdProperty, DateTimeProperty, RelationshipTo,
  BooleanProperty)
from itertools import chain
from config import app_config
import hashlib
import app

from relations.vote import VoteRelationship
from relations.comment import CommentRelationship

from common import CommentalityModel

class User(CommentalityModel):
  number = StringProperty()
  code = StringProperty()
  is_superuser = BooleanProperty(default=False)
  comments = RelationshipFrom('comment.models.Comment', 'OWNED_BY', model=CommentRelationship)
  votes = RelationshipTo('comment.models.Comment', 'VOTED_FOR', model=VoteRelationship)
  media_properties = RelationshipFrom('media_property.models.MediaProperty', 'EDITED_BY')
  banned_on = RelationshipTo('media_property.models.MediaProperty', 'BANNED_ON')

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

  def has_commented_on_article(self, article):
    for comment in chain(article.visible_comments, article.hidden_comments):
      if comment.owner.is_connected(self):
        return True
    return False

  def is_editor_on_article(self, article):
    return article.owner.single().editors.is_connected(self)

  def has_voted_on_all_comments(self, article):
    for comment in article.visible_comments:
      if not comment.voters.is_connected(self):
        return False
    return True
