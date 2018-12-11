from neomodel import (StructuredNode, StringProperty, RelationshipFrom,
  UniqueIdProperty, DateTimeProperty, One)

class Article(StructuredNode):
  uid = UniqueIdProperty()
  created_at = DateTimeProperty(default_now=True)
  modified_at = DateTimeProperty(default_now=True)

  external_id = StringProperty(required=True)
  comments = RelationshipFrom('comment.models.Comment', 'POSTED_ON')

  @staticmethod
  def get_all():
    return Article.nodes

  @staticmethod
  def get(uid):
    return Article.nodes.get_or_none(uid=uid)

  def __repr__(self):
    return '<Article({name!r})>'.format(name=self.external_id)

  @staticmethod
  def get_by_external_id(external_id):
    return Article.nodes.get_or_none(external_id=external_id)
