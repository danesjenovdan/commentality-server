from marshmallow import Schema, fields


class ArticleSchema(Schema):
  uid = fields.Str(dump_only=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)

  title = fields.Str(required=True)
  external_id = fields.Str(required=True)
  owner = fields.Function(lambda obj: obj.owner.single().name)
  visible = fields.Nested('comment.serializers.CommentSchema',
                          many=True, exclude=('owner', ), dump_only=True)

  can_vote = fields.Boolean(required=False)
  can_comment = fields.Boolean(required=False)


class AuthenthicatedArticleSchema(ArticleSchema):
  visible = fields.Nested('comment.serializers.AuthenticatedCommentSchema',
                          many=True, exclude=('owner', ), dump_only=True)

article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)
authenthicated_article_schema = AuthenthicatedArticleSchema()
