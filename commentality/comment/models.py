from flask import g
from neomodel import (StructuredNode, StringProperty, RelationshipTo,
  RelationshipFrom, UniqueIdProperty, DateTimeProperty, BooleanProperty, One)
from relations.vote import VoteRelationship
from relations.comment import CommentRelationship
from common import CommentalityModel

class Comment(CommentalityModel):
  contents = StringProperty(required=True)
  owner = RelationshipTo('user.models.User', 'OWNED_BY', cardinality=One, model=CommentRelationship)
  article = RelationshipTo('article.models.Article', 'POSTED_ON')
  hidden = RelationshipTo('article.models.Article', 'HIDDEN_ON')
  voters = RelationshipFrom('user.models.User', 'VOTED_FOR', model=VoteRelationship)
  pending = BooleanProperty(default=True)

  @property
  def votes(self):
    votes = { 'like': 0, 'meh': 0, 'dislike': 0 }
    for voter in self.voters:
      vote = self.voters.relationship(voter)
      votes[vote.type] += 1
    return votes

  @property
  def voter_ids(self):
    return [voter.uid for voter in self.voters]

  @property
  def voter_count(self):
    return len(self.voters)

  def update(self, data):
    for name, value in data.items():
      setattr(self, name, value)
    self.save()
