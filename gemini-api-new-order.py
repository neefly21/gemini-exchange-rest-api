import requests
import json
import base64
import hmac
import hashlib
import datetime, time
import const
import time

def createBuyRequest(requestType):
    successfullyMadeOrder = False
    isFirstAttempt = True
    numOfAttempts = 0
    base_url = const.url
    endpoint = "/v1/order/new"
    url = base_url + endpoint
    gemini_api_key = const.gemini_api_key
    gemini_api_secret = const.gemini_api_secret
    t = datetime.datetime.now()
    payload_nonce = str(int(time.mktime(t.timetuple())*1000))

    while(successfullyMadeOrder == False):
        if isFirstAttempt == False:
            time.sleep(2.5)
            t = datetime.datetime.now()
            payload_nonce = str(int(time.mktime(t.timetuple())*1000))

        response = requests.get(base_url + "/v1/pubticker/btcusd")
        btc_data = response.json()

        orderSizeInUSD = 100.0 # default is $100 
        mostRecentSalePrice = float(btc_data['last'])-5
        orderQuantity = orderSizeInUSD / mostRecentSalePrice

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
            "side": "sell",
            "type": "exchange limit",
            "options": ["fill-or-kill"] 
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
    
        print('\n\n')
        print(new_order)

        result = new_order['is_cancelled']

        if result == True:
            print('\nOrder is cancelled!')
            numOfAttempts += 1
            isFirstAttempt = False
            continue

        return response.json()
    

createBuyRequest("sell")