from marshmallow import Schema, fields


class UserSchema(Schema):
  uid = fields.String()
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)

  number = fields.String(load_only=True)
  comments = fields.Nested('comment.serializers.CommentSchema',
                           many=True, exclude=('owner', ), dump_only=True)

user_schema = UserSchema()
