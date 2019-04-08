from twilio.rest import Client
import random

from config import app_config

def send_confirmation_code(to_number):
    verification_code = _generate_code()
    number = _send_sms(to_number, 'Tvoje enkratno geslo za Commentality je ' + str(verification_code))
    return (verification_code, number)

def _generate_code():
    return str(random.randrange(100000, 999999))

def _send_sms(to_number, body):
    account_sid = app_config['development'].TWILIO_ACCOUNT_SID
    auth_token = app_config['development'].TWILIO_AUTH_TOKEN
    twilio_number = app_config['development'].TWILIO_NUMBER
    client = Client(account_sid, auth_token)
    message = client.api.messages.create(to_number,
                           from_=twilio_number,
                           body=body)
    return message.to
