import requests
import json
import base64
import hmac
import hashlib
import time
import const
import time
from datetime import datetime
import gemini_api_helper as gemini

url_parameters = "/v1/mytrades"
trades = gemini.make_request_to_api(url_parameters)
trades.sort(key=gemini.extract_time, reverse=True)
recent_eth_trades = []

# https://stackoverflow.com/questions/56640492/python-get-a-value-in-json-array
for trade in trades:
    trade_coin = trade["symbol"]
    if(trade_coin.lower() == 'ethusd'):
        recent_eth_trades.append(trade)

print(recent_eth_trades)
