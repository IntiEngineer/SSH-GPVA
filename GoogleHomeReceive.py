import requests
import time
import json
import os
from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)
@app.route('/',methods=['POST'])
def index():
    req = request.get_json(silent=True, force=True)
    val = processRequest(req)
    r = make_response(json.dumps(val))
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    message = req['message']
    if message=='help':
        status = open("GoogleHomeStatus.txt",'w')
        status.write('help')
        status.close()
    return {
    "speech": "it is done",
    "displayText": "it is done",
    "source": "apiai-weather-webhook-sample"
    }

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5000)