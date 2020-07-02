import datetime
import time

from app import db
from app.models import XqcRate

from settings_local import STORAGE_INTERVAL, DELETER_TIMEOUT

if __name__ == '__main__':
    while True:
        old_records = XqcRate.query.filter(
            XqcRate.timestamp < datetime.datetime.now().timestamp() - STORAGE_INTERVAL).all()

        for old_record in old_records:
            print('deleting', old_record.__dict__, flush=True)
            db.session.delete(old_record)
            db.session.commit()
            print('deleted\n', flush=True)

        time.sleep(DELETER_TIMEOUT)
