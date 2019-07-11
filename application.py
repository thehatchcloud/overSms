from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    return 'This app returns information over text message.'

@app.route("/directions", methods=['POST'])
def directions():
    """Respond to incoming calls with a simple text message."""

    resp = MessagingResponse()

    body = request.values.get('Body', None).lower()
    if body == 'ask':
        message = 'To ask for directions, enter: from: <point 1> to: <point 2>' 
    
    # Check for from: and to: in the string
    if 'from:' in body and 'to:' in body:
        body = body.replace('from: ', 'from:').replace('to: ', 'to:')
        to_location = body.find('to:')
        wp0 = body[5:to_location-1]
        wp1 = body[to_location+3:]

        message = f'wp0 is {wp0}\nwp1 is {wp1}'
    
    else:
        message = "I don't know what you said. Enter 'ask' for help."
        resp.message(message)
        return str(resp)



    resp.message(message)
    return str(resp)