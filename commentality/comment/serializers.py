from marshmallow import fields, Schema

class CommentSchema(Schema):
  id = fields.Int(dump_only=True)
  contents = fields.Str(required=True)
  owner_id = fields.Int(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)

comment_schema = CommentSchema()
comment_schemas = CommentSchema(many=True)
