from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return 'This app returns information over text message.'