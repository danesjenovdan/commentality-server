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
  votes = fields.Method(serialize='get_votes', dump_only=True)

  def get_votes(self, obj):
    votes = { 'like': [], 'meh': [], 'dislike': [] }
    for voter in obj.voters:
      vote = obj.voters.relationship(voter)
      votes[vote.type].append(voter.uid)
    return votes

comment_schema = CommentSchema()
