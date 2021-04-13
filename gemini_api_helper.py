import requests
import json
import base64
import hmac
import hashlib
import time
import const
import time
from datetime import datetime

url = const.url
gemini_api_key = const.gemini_api_key
gemini_api_secret = const.gemini_api_secret
session = requests.Session()
discord_webhook = const.discord_webhook_url

#"/v1/mytrades"
def make_request_to_api(url_parameters, payload):
    request_headers = create_request_headers(url_parameters, payload)
    response = session.post(url + url_parameters, headers=request_headers)
    return response.json()

def create_request_headers(request_url, payload):
    t = datetime.now()
    payload_nonce =  str(int(time.mktime(t.timetuple())*1000))
    encoded_payload = json.dumps(payload).encode()
    b64 = base64.b64encode(encoded_payload)
    signature = hmac.new(gemini_api_secret, b64, hashlib.sha384).hexdigest()

    return {
        'Content-Type': "text/plain",
        'Content-Length': "0",
        'Access-Control-Allow-Origin': "*",
        'X-GEMINI-APIKEY': gemini_api_key,
        'X-GEMINI-PAYLOAD': b64,
        'X-GEMINI-SIGNATURE': signature,
        'Cache-Control': "no-cache"
        }

# example of how to create the payloads for the Gemini API - utilize in write-up on github
def create_basic_payload():
    t = datetime.now()
    payload_nonce = str(int((time.mktime(t.timetuple())*1000)))

    return {"request": "/v1/mytrades", "nonce": payload_nonce}

def create_complex_payload(parameter_json):
    t = datetime.now()
    payload_nonce = str(int((time.mktime(t.timetuple())*1000)+2))

    return {
            "request": "/v1/order/new",
            "nonce": payload_nonce,
            "symbol": parameter_json['currency'],
            "amount": parameter_json['coin_amount'],
            "price": parameter_json['most_recent_price'],
            "side": parameter_json['request_side'],
            "type": "exchange limit",
            "options": ["fill-or-kill"] 
        }

#notify a discord server
def send_discord_notification(content):
    payload = {'content': content}
    response = session.post(discord_webhook, payload)

# https://stackoverflow.com/questions/26924812/python-sort-list-of-json-by-value
def extract_time(json):
    try:
        return int(json['timestamp'])
    except KeyError:
        return 0