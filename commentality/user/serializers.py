from marshmallow import fields

from commentality.base import BaseSchema


class UserSchema(BaseSchema):
  name = fields.Str(required=True)
  email = fields.Email(required=True)
  password = fields.Str(required=True, load_only=True)
  comments = fields.Nested('commentality.comment.serializers.CommentSchema',
                           many=True, exclude=('owner', ), dump_only=True)

user_schema = UserSchema()
