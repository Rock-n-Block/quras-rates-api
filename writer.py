import requests
import datetime
import json

from app import db
from app.models import XqcRate

from settings_local import STORAGE_INTERVAL, API_URL


if __name__ == '__main__':
    now_ts = datetime.datetime.now().timestamp()
    start_ts = now_ts - STORAGE_INTERVAL
    usd_rate_info = json.loads(requests.get(
        API_URL + 'quras-token/market_chart/range?vs_currency={}&from={}&to={}'.format('usd', start_ts,
                                                                                       now_ts)).content.decode())
    jpy_rate_info = json.loads(requests.get(
        API_URL + 'quras-token/market_chart/range?vs_currency={}&from={}&to={}'.format('jpy', start_ts,
                                                                                       now_ts)).content.decode())

    usd_rates = usd_rate_info['prices']
    jpy_rates = jpy_rate_info['prices']
    print('usd rates', usd_rates, flush=True)
    print('jpy_rates', jpy_rates, flush=True)

    for usd_rate, jpy_rate in zip(usd_rates, jpy_rates):
        new_rate = XqcRate(timestamp=usd_rate[0]//1000, usd_rate=usd_rate[1], jpy_rate=jpy_rate[1])
        db.session.add(new_rate)
        db.session.commit()
