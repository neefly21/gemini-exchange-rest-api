import requests, json, base64,hmac ,hashlib ,time, const
from datetime import datetime
import gemini_api_helper as gemini

def create_new_order_request(buy_request):
    successfullyMadeOrder = False
    isFirstAttempt = True
    numOfAttempts = 0
    endpoint = "/v1/order/new"
    currency = buy_request['currency']
    payload = gemini.create_basic_payload()
    
    most_recent_trade = gemini.make_request_to_api("/v1/mytrades", payload)
    most_recent_trade.sort(key=gemini.extract_time, reverse=True)

    currency_qty_rounding = 8 if currency == "btcusd" else 5
    order_quantity = float(buy_request['amount_in_usd']) / float(most_recent_trade[0]['price']) 
    coin_amount = round(order_quantity, currency_qty_rounding)

    payload_params_json = {
        "currency": currency,
        "coin_amount": coin_amount,
        "most_recent_price": most_recent_trade[0]['price'],
        "request_side": buy_request['side']
    }

    order_request_payload = gemini.create_complex_payload(payload_params_json)
    json_response = gemini.make_request_to_api("/v1/order/new", order_request_payload)

    print(json_response)

buy_request = {
    "side": "sell",
    "currency": "ethusd",
    "amount_in_usd": 100.0 # Default is $100
}

create_new_order_request(buy_request)