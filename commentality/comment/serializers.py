from marshmallow import fields, Schema

class CommentSchema(Schema):
  uid = fields.Str(dump_only=True)
  contents = fields.Str(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
  owner = fields.Function(lambda obj: obj.owner[0].name)

comment_schema = CommentSchema()
