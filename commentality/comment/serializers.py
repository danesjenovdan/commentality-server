from marshmallow import Schema, fields


class CommentSchema(Schema):
  uid = fields.Str(dump_only=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)

  contents = fields.Str(required=True)
  owner = fields.Function(lambda obj: obj.owner[0].name)
  article_external_id = fields.Function(
    lambda obj: obj.article[0].external_id,
  )
  vote_count = fields.Method(serialize='get_vote_count', dump_only=True)

  def get_vote_count(self, obj):
    votes = { 'like': 0, 'meh': 0, 'dislike': 0 }
    for voter in obj.voters:
      vote = obj.voters.relationship(voter)
      votes[vote.type] += 1
    return votes

comment_schema = CommentSchema()
