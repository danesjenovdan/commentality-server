from neomodel import (StringProperty, RelationshipTo, One)

from commentality.base import BaseModel


class Comment(BaseModel):
  contents = StringProperty(required=True)
  owner = RelationshipTo('commentality.user.models.User', 'OWNED_BY', cardinality=One)
  article = RelationshipTo('commentality.article.models.Article', 'POSTED_ON', cardinality=One)

  def __repr__(self):
    return '<Comment {}>'.format(self.uid)
