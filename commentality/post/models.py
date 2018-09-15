import datetime as dt
from commentality.extensions import db

class Post(db.Model):
  __tablename__ = 'posts'

  id = db.Column(db.Integer, primary_key=True)
  contents = db.Column(db.Text, nullable=False)
  owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  created_at = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
  modified_at = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)

  def __init__(self, data):
    self.contents = data.get('contents')
    self.owner_id = data.get('owner_id')

  @staticmethod
  def get_all_posts():
    return Post.query.all()

  @staticmethod
  def get_one_post(id):
    return Post.query.get(id)

  def __repr__(self):
    return '<id {}>'.format(self.id)
