from marshmallow import Schema, fields


class ArticleSchema(Schema):
  uid = fields.Str(dump_only=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)

  title = fields.Str(required=True)
  comments = fields.Nested('comment.serializers.CommentSchema',
                           many=True, exclude=('owner', ), dump_only=True)

article_schema = ArticleSchema()
