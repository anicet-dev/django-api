import os
from twilio.rest import Client

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")

def send_sms(to, body):
    if not (TWILIO_SID and TWILIO_TOKEN and TWILIO_PHONE):
        print("Twilio not configured. SMS not sent to", to)
        return None
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    message = client.messages.create(body=body, from_=TWILIO_PHONE, to=to)
    return message.sid
