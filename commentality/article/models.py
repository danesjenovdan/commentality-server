from neomodel import (StructuredNode, StringProperty, RelationshipFrom,
  UniqueIdProperty, DateTimeProperty, One, RelationshipTo, BooleanProperty)

class Article(StructuredNode):
  uid = UniqueIdProperty()
  created_at = DateTimeProperty(default_now=True)
  modified_at = DateTimeProperty(default_now=True)

  external_id = StringProperty(required=True)
  title = StringProperty(required=True)
  owner = RelationshipTo('media_property.models.MediaProperty', 'OWNED_BY', cardinality=One)
  visible = RelationshipFrom('comment.models.Comment', 'POSTED_ON')
  hidden = RelationshipFrom('comment.models.Comment', 'HIDDEN_ON')

  can_vote = BooleanProperty(default=True)
  can_comment = BooleanProperty(default=True)

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

  def update(self, data):
    for name, value in data.items():
      setattr(self, name, value)
    self.save()
