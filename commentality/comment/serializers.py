from marshmallow import Schema, fields


class CommentSchema(Schema):
  uid = fields.Str(dump_only=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)

  contents = fields.Str(required=True)
  owner = fields.Function(lambda obj: obj.owner.single().name)
  article_uid = fields.Function(
    lambda obj: obj.article.single().uid,
  )
  votes = fields.Method(serialize='get_votes', dump_only=True)

  def get_votes(self, obj):
    votes = {
      'like': obj.cypher('MATCH (n)<-[r]-() WHERE n.uid = "' + obj.uid + '" AND r.type="like" RETURN COUNT(r)')[0][0][0],
      'meh': obj.cypher('MATCH (n)<-[r]-() WHERE n.uid = "' + obj.uid + '" AND r.type="meh" RETURN COUNT(r)')[0][0][0],
      'dislike': obj.cypher('MATCH (n)<-[r]-() WHERE n.uid = "' + obj.uid + '" AND r.type="dislike" RETURN COUNT(r)')[0][0][0]
    }
    return votes


class AuthenticatedCommentSchema(CommentSchema):
  my_vote = fields.Method(serialize='get_my_vote', dump_only=True)

  def get_my_vote(self, obj):
    return [voter.uid for voter in obj.voters]


comment_schema = CommentSchema()
authenticated_comment_schema = AuthenticatedCommentSchema()
