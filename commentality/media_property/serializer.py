from marshmallow import Schema, fields


class MediaPropertySchema(Schema):
  uid = fields.Str()
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)

  name = fields.Str(load_only=True)
  articles = fields.Nested('article.serializers.ArticleSchema',
                           many=True, exclude=('owner', ), dump_only=True)

media_peroperty_schema = MediaPropertySchema()
