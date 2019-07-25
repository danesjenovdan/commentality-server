import app
from neomodel import (StructuredNode, StringProperty, RelationshipFrom,
  UniqueIdProperty, DateTimeProperty, One, RelationshipTo, BooleanProperty)
from common import CommentalityModel

class Article(CommentalityModel):
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
      commenters.add(comment.owner.single().uid)
    return commenters

  @property
  def commenter_count(self):
    return len(self.commenters)

  @property
  def voter_count(self):
    count = 0
    for comment in self.visible_comments:
      if count < comment.voter_count:
        count = comment.voter_count

    return count

  @staticmethod
  def get_by_title(title):
    return Article.nodes.get_or_none(title=title)

  def update(self, data):
    for name, value in data.items():
      setattr(self, name, value)
    self.save()
