from marshmallow import Schema, fields


class ArticleSchema(Schema):
  uid = fields.String(dump_only=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)

  title = fields.String()
  owner = fields.Function(lambda obj: obj.owner.single().name)
  visible_comments = fields.Nested('comment.serializers.CommentSchema',
                                  many=True, exclude=('owner', ), dump_only=True)
  hidden_comments = fields.Nested('comment.serializers.CommentSchema',
                                  many=True, exclude=('owner', ), dump_only=True)
  comments_voted_on = fields.String(many=True)
  can_vote = fields.Boolean()
  can_comment = fields.Boolean()

article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)
