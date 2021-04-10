import requests
import json
import base64
import hmac
import hashlib
import datetime, time
import const

base_url = "https://api.sandbox.gemini.com"
url = "https://api.sandbox.gemini.com"
endpoint = "/v1/order/new"
url = base_url + endpoint

gemini_api_key = const.gemini_api_key
gemini_api_secret = const.gemini_api_secret

t = datetime.datetime.now()
payload_nonce =  str(int(time.mktime(t.timetuple())*1000))

response = requests.get(base_url + "/v1/pubticker/btcusd")
btc_data = response.json()

orderSize = 100.0
mostRecentSalePrice = float(btc_data['last'])
orderQuantity = orderSize / mostRecentSalePrice

print("Current Price:" )
print(mostRecentSalePrice)

print("Calculated Order Quantity:")
print(orderQuantity)

payload = {
   "request": "/v1/order/new",
    "nonce": payload_nonce,
    "symbol": "btcusd",
    "amount": round(orderQuantity, 8),
    "price": mostRecentSalePrice,
    "side": "buy",
    "type": "exchange limit",
    "options": ["maker-or-cancel"] 
}

encoded_payload = json.dumps(payload).encode()
b64 = base64.b64encode(encoded_payload)
signature = hmac.new(gemini_api_secret, b64, hashlib.sha384).hexdigest()

request_headers = { 'Content-Type': "text/plain",
                    'Content-Length': "0",
                    'X-GEMINI-APIKEY': gemini_api_key,
                    'X-GEMINI-PAYLOAD': b64,
                    'X-GEMINI-SIGNATURE': signature,
                    'Cache-Control': "no-cache" }

response = requests.post(url,
                        data=None,
                        headers=request_headers)

new_order = response.json()
print(new_order)