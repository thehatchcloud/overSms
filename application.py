from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from bingmaps import Map
import os

app = Flask(__name__)
bing_map = Map(os.environ['BING_MAPS_KEY'])

@app.route('/')
def index():
    return '<h1>overSmsApp</h1><p>This app returns information over text message.</p>'

@app.route("/directions", methods=['POST'])
def directions():
    """Respond to incoming calls with a simple text message."""

    resp = MessagingResponse()

    body = request.values.get('Body', None).lower()
    if body == 'ask':
        message = 'To ask for directions, enter: from: <point 1> to: <point 2>' 
    
    # Check for from: and to: in the string
    elif 'from:' in body and 'to:' in body:
        message = bing_map.get_directions(body)
    
    else:
        message = "I don't know what you said. Enter 'ask' for help."

    resp.message(message)
    return str(resp)
