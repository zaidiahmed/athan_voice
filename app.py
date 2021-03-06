#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


# http://api.aladhan.com/timingsByCity?city=Dubai&country=AE&method=2

def processRequest(req):
    baseurl = "http://api.aladhan.com/timingsByCity?city=Dallas&country=USA&method=2"
    result = urllib.urlopen(baseurl).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res

def makeWebhookResult(data):
    adata = data.get('data')
    if adata is None:
        return {}

    timings = adata.get('timings')
    if timings is None:
        return {}

    #get fajr
    fajr = timings.get("Fajr")
    if (fajr is None):
        return {}

    speech = "Today Fajr is at ", fajr

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
         "data": {},
         "contextOut": [],
        "source": "prayer-times-api"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
