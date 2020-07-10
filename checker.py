import requests
import json
import datetime
import time
import traceback
import sys

from app import db
from app.models import XqcRate
from settings_local import CHECKER_TIMEOUT, API_URL

if __name__ == '__main__':
    while True:
        try:
            coin_info = json.loads(requests.get(API_URL + 'quras-token').content.decode())
            timestamp = int(datetime.datetime.now().timestamp())
            usd_rate = coin_info['market_data']['current_price']['usd']
            jpy_rate = coin_info['market_data']['current_price']['jpy']
            new_rate = XqcRate(timestamp=timestamp, usd_rate=usd_rate, jpy_rate=jpy_rate)
            db.session.add(new_rate)
            db.session.commit()

            print('new rates at {}: usd {}, jpy {}'.format(timestamp, usd_rate, jpy_rate), flush=True)
        except json.decoder.JSONDecodeError as e:
            print('\n'.join(traceback.format_exception(*sys.exc_info())), flush=True)
        except Exception as e:
            print('\n'.join(traceback.format_exception(*sys.exc_info())), flush=True)
            print('NEW UNEXPECTED ERROR', flush=True)

        time.sleep(CHECKER_TIMEOUT)
