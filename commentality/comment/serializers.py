from marshmallow import Schema, fields


class CommentSchema(Schema):
  uid = fields.Str(dump_only=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)

  contents = fields.Str(required=True)
  owner = fields.Function(lambda obj: obj.owner[0].name)
  article = fields.Number(load_only=True, required=True)
  article_external_id = fields.Function(lambda obj: obj.article[0].external_id)

comment_schema = CommentSchema()
