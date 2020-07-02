import requests
import json
import datetime
import time

from app import db
from app.models import XqcRate
from settings_local import CHECKER_TIMEOUT, API_URL

if __name__ == '__main__':
    while True:
        coin_info = json.loads(requests.get(API_URL + 'quras-token').content.decode())
        timestamp = int(datetime.datetime.now().timestamp())
        usd_rate = coin_info['market_data']['current_price']['usd']
        jpy_rate = coin_info['market_data']['current_price']['jpy']
        new_rate = XqcRate(timestamp=timestamp, usd_rate=usd_rate, jpy_rate=jpy_rate)
        db.session.add(new_rate)
        db.session.commit()

        print('new rates at {}: usd {}, jpy {}'.format(timestamp, usd_rate, jpy_rate), flush=True)

        time.sleep(CHECKER_TIMEOUT)
