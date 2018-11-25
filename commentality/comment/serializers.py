from marshmallow import fields, Schema

class CommentSchema(Schema):
  uid = fields.Str(dump_only=True)
  contents = fields.Str(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
  owner = fields.Nested('commentality.user.serializers.UserSchema',
                        exclude=('comments', ), dump_only=True)

comment_schema = CommentSchema()
