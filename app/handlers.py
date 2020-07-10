import datetime
from flask import jsonify
from flask import request
import json
from flask import make_response

from app import app
from app import db
from app.models import XqcRate

from settings_local import TIME_INTERVAL


@app.route('/api/v1/rates/xqc', methods=['GET'])
def rates():
    xqc_rate = db.session.query(XqcRate).order_by(XqcRate.timestamp.desc()).first()
    if xqc_rate:
        # print('\nrate object', xqc_rate.__dict__, flush=True)

        rates = []
        rates.append({'code': 'USD', 'name': 'US Dollar', 'rate': xqc_rate.usd_rate})
        rates.append({'code': 'JPY', 'name': 'Japanese Yen', 'rate': xqc_rate.jpy_rate})

        # print('rates', rates, flush=True)

        return jsonify(rates)

    print('\n{}: Not found actual at {}'.format(datetime.datetime.now(), datetime.datetime.now().timestamp()),
          flush=True)


@app.route('/api/v1/historical-rates/<currency>')
def historical_rates(currency):
    request_ts = int(request.args.get('ts'))
    # print('\nnew request', request_ts, currency, flush=True)

    start_ts = request_ts // 1000 - TIME_INTERVAL
    end_ts = request_ts // 1000 + TIME_INTERVAL
    # print('start_ts', start_ts, flush=True)
    # print('end_ts', end_ts, flush=True)
    ts_rates = XqcRate.query.filter(XqcRate.timestamp > start_ts, XqcRate.timestamp < end_ts).order_by(
        XqcRate.timestamp.desc()).first()
    if ts_rates:
        if currency == 'USD':
            rate = ts_rates.usd_rate
        elif currency == 'JPY':
            rate = ts_rates.jpy_rate
        else:
            rate = None

        result = {
            'ts': request_ts,
            'fetchedOn': ts_rates.timestamp * 1000,
            'rate': rate
        }

        # print('result', result, flush=True)

        return jsonify(result)

    print('{}: Not found historical rates at {}'.format(datetime.datetime.now(), request_ts), flush=True)
    result = {
        'ts': request_ts
    }

    return jsonify(result)
