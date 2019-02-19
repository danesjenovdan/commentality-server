from marshmallow import Schema, fields
from flask import g

class VotesSchema(Schema):
  like = fields.Integer()
  meh = fields.Integer()
  dislike = fields.Integer()

class CommentSchema(Schema):
  uid = fields.Str(dump_only=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
  contents = fields.Str(required=True)
  owner = fields.Function(lambda obj: obj.owner.single().name)
  article_uid = fields.Function(lambda obj: obj.article.single().uid,)
  current_user_voted = fields.String()
  votes = fields.Nested(VotesSchema())

comment_schema = CommentSchema()
