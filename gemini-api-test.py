import requests
import json
import base64
import hmac
import hashlib
import datetime, time
import const

t = datetime.datetime.now()
payload_nonce =  str(int(time.mktime(t.timetuple())*1000))
payload =  {"request": "/v1/mytrades", "nonce": payload_nonce}
encoded_payload = json.dumps(payload).encode()
b64 = base64.b64encode(encoded_payload)
signature = hmac.new(const.gemini_api_secret, b64, hashlib.sha384).hexdigest()

request_headers = {
    'Content-Type': "text/plain",
    'Content-Length': "0",
    'X-GEMINI-APIKEY': const.gemini_api_key,
    'X-GEMINI-PAYLOAD': b64,
    'X-GEMINI-SIGNATURE': signature,
    'Cache-Control': "no-cache"
    }

response = requests.post(const.url, headers=request_headers)

print(response.json())