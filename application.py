from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return 'This app returns information over text message.'

@app.route('/directions')
def directions():
    return 'This url will return directions to the user'