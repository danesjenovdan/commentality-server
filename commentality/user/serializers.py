from marshmallow import Schema, fields


class UserSchema(Schema):
  uid = fields.Str(dump_only=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)

  name = fields.Str(required=True)
  email = fields.Email(required=True)
  password = fields.Str(required=True, load_only=True)
  comments = fields.Nested('comment.serializers.CommentSchema',
                           many=True, exclude=('owner', ), dump_only=True)

user_schema = UserSchema()
