from marshmallow import Schema, fields


class MediaPropertySchema(Schema):
  uid = fields.String()
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)

  name = fields.String()
  articles = fields.Nested('article.serializers.ArticleSchema',
                           many=True, exclude=('owner', ), dump_only=True)

media_peroperty_schema = MediaPropertySchema()
