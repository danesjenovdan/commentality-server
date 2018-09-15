from marshmallow import fields, Schema
from commentality.post.serializers import PostSchema

class UserSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.Str(required=True)
  email = fields.Email(required=True)
  password = fields.Str(required=True, load_only=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
  posts = fields.Nested(PostSchema, many=True)

user_schema = UserSchema()
user_schemas = UserSchema(many=True)
