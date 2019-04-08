from marshmallow import Schema, fields
from flask import g

class VotesSchema(Schema):
  like = fields.Integer()
  meh = fields.Integer()
  dislike = fields.Integer()

class CommentSchema(Schema):
  uid = fields.String(dump_only=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
  contents = fields.String(required=True)
  owner = fields.Function(lambda obj: obj.owner.single().name)
  article_uid = fields.Function(lambda obj: obj.article.single().uid,)
  voter_ids = fields.List(fields.String(), dump_only=True)
  votes = fields.Nested(VotesSchema())
  voter_count = fields.Integer()
  visible = fields.Function(lambda obj: True if obj.article.single() else False)
  hidden = fields.Function(lambda obj: True if obj.hidden.single() else False)
  pending = fields.Boolean()

comment_schema = CommentSchema()
