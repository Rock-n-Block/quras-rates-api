from flask import Flask, jsonify
import requests
import json

app = Flask(__name__)

api_url = 'https://api.coingecko.com/api/v3/coins/'

tsyms = [
    {
        'code': 'USD',
        'name': 'US Dollar'
    },
    {
        'code': 'JPY',
        'name': 'Japanese Yen'
    }
]

fsyms = {
    'xqc': 'quras-token'
}


@app.route('/api/v1/rates/<currency>', methods=['GET'])
def rates(currency):
    coin_info = json.loads(requests.get(api_url + fsyms[currency]).content.decode())
    rates = []
    for tsym in tsyms:
        rates.append({
            'code': tsym['code'],
            'name': tsym['name'],
            'rate': coin_info['market_data']['current_price'][tsym['code'].lower()]
        })

    print('rates', rates, flush=True)

    return jsonify(rates)
