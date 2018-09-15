from marshmallow import fields, Schema

class PostSchema(Schema):
  id = fields.Int(dump_only=True)
  contents = fields.Str(required=True)
  owner_id = fields.Int(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)

post_schema = PostSchema()
post_schemas = PostSchema(many=True)
