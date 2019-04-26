from flask import json, Response
from neomodel import StructuredNode, UniqueIdProperty, DateTimeProperty

def custom_response(res, status_code):
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )

class CommentalityModel(StructuredNode):
  __abstract_node__ = True
  uid = UniqueIdProperty()
  created_at = DateTimeProperty(default_now=True)
  modified_at = DateTimeProperty(default_now=True)

  @classmethod
  def get_all(cls):
    return cls.nodes

  @classmethod
  def get(cls, uid):
    return cls.nodes.get_or_none(uid=uid)

  def __repr__(self):
    return f'<{self.__class__.__name__} {self.uid}>'
