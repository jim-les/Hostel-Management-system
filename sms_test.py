import os
from twilio.rest import Client
account_sid = os.environ['VA88df60adaacfcf65889d43525fdbf5d3']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

message = client.messages \
    .create(
         body='This is the ship that made the Kessel Run in fourteen parsecs?',
         from_='+15017122661',
         to='+15558675310'
     )

print(message.sid)