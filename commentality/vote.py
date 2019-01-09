from neomodel import StructuredRel, StringProperty


class VoteRelationship(StructuredRel):
    type = StringProperty(
      choices={'like': 'like', 'dislike': 'dislike', 'meh': 'meh'}
    )
