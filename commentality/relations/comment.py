from neomodel import StructuredRel, BooleanProperty

class CommentRelationship(StructuredRel):
    is_visible = BooleanProperty(default=True)
