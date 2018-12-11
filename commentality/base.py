from neomodel import StructuredNode, DateTimeProperty, UniqueIdProperty
from marshmallow import fields, Schema


class BaseModel(StructuredNode):
  uid = UniqueIdProperty()
  created_at = DateTimeProperty(default_now=True)
  modified_at = DateTimeProperty(default_now=True)

  @staticmethod
  def get_all():
    return BaseModel.nodes

  @staticmethod
  def get(uid):
    return BaseModel.nodes.get_or_none(uid=uid)


class BaseSchema(Schema):
  uid = fields.Str(dump_only=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
