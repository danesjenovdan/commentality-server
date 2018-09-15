import datetime as dt
from commentality.extensions import db, bcrypt

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), unique=True, nullable=False)
  email = db.Column(db.String(128), unique=True, nullable=False)
  password = db.Column(db.Binary(128), nullable=False)
  created_at = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
  modified_at = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
  posts = db.relationship('Post', backref='users', lazy=True)

  def __init__(self, name, email, password=None, **kwargs):
    db.Model.__init__(self, name=name, email=email, **kwargs)
    if password:
      self.set_password(password)
    else:
      self.password = None

  def set_password(self, password):
    self.password = bcrypt.generate_password_hash(password)

  def check_password(self, value):
    return bcrypt.check_password_hash(self.password, value)

  def __repr__(self):
    return '<User({name!r})>'.format(name=self.name)

  @staticmethod
  def get_all_users():
    return User.query.all()

  @staticmethod
  def get_one_user(id):
    return User.query.get(id)

  @staticmethod
  def get_user_by_email(value):
    return User.query.filter_by(email=value).first()


