from flask import g
from neomodel import (StructuredNode, StringProperty, RelationshipTo,
  RelationshipFrom, UniqueIdProperty, DateTimeProperty, BooleanProperty, One)
from relations.vote import VoteRelationship
from relations.comment import CommentRelationship

class Comment(StructuredNode):
  uid = UniqueIdProperty()
  created_at = DateTimeProperty(default_now=True)
  modified_at = DateTimeProperty(default_now=True)

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
