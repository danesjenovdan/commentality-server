import os

class Config(object):
  DEBUG = False
  TESTING = False
  JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
  DATABASE_URL = os.getenv('DATABASE_URL')
class Development(Config):
  DEBUG = True

class Production(Config):
  pass

app_config = {
  'development': Development,
  'production': Production,
}
