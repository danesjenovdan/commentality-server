from marshmallow import fields, Schema
from commentality.comment.serializers import CommentSchema

class UserSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.Str(required=True)
  email = fields.Email(required=True)
  password = fields.Str(required=True, load_only=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
  comments = fields.Nested(CommentSchema, many=True)

user_schema = UserSchema()
user_schemas = UserSchema(many=True)
