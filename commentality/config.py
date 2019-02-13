import os

class Config(object):
  DEBUG = False
  TESTING = False
  SESSION_TYPE = 'filesystem'
  JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
  DATABASE_URL = os.getenv('DATABASE_URL')
  TWILIO_ACCOUNT_SID = ''
  TWILIO_AUTH_TOKEN = ''
  TWILIO_NUMBER = ''
class Development(Config):
  DEBUG = True
  SECRET_KEY = 'no secrets'

class Production(Config):
  SECRET_KEY = 'please set a secret'
  pass

app_config = {
  'development': Development,
  'production': Production,
}
