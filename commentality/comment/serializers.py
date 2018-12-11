from marshmallow import fields

from commentality.base import BaseSchema


class CommentSchema(BaseSchema):
  contents = fields.Str(required=True)
  owner = fields.Function(lambda obj: obj.owner[0].name)

comment_schema = CommentSchema()
