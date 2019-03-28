import app
from neomodel import (StructuredNode, StringProperty, RelationshipFrom,
  UniqueIdProperty, DateTimeProperty, One, RelationshipTo, BooleanProperty)

class Article(StructuredNode):
  uid = UniqueIdProperty()
  created_at = DateTimeProperty(default_now=True)
  modified_at = DateTimeProperty(default_now=True)

  title = StringProperty(required=True)
  owner = RelationshipTo('media_property.models.MediaProperty', 'OWNED_BY', cardinality=One)
  visible_comments = RelationshipFrom('comment.models.Comment', 'POSTED_ON')
  hidden_comments = RelationshipFrom('comment.models.Comment', 'HIDDEN_ON')

  can_vote = BooleanProperty(default=True)
  can_comment = BooleanProperty(default=True)

  @property
  def commenters(self):
    commenters = set()
    for comment in self.visible_comments:
      app.app.logger.info(comment.owner.single().uid)

      commenters.add(comment.owner.single().uid)
    return commenters

  @staticmethod
  def get_all():
    return Article.nodes

  @staticmethod
  def get(uid):
    return Article.nodes.get_or_none(uid=uid)
  
  @staticmethod
  def get_by_title(title):
    return Article.nodes.get_or_none(title=title)

  def __repr__(self):
    return '<Article({name!r})>'.format(name=self.title)

  def update(self, data):
    for name, value in data.items():
      setattr(self, name, value)
    self.save()
