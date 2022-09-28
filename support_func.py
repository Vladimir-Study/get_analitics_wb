from datetime import datetime, timedelta
from pprint import pprint
import asyncio
import os


def insert_date() -> dict:
    date_to = datetime.now()
    date_from = date_to + timedelta(days=-28)
    return {'date_to': date_to.date().strftime('%Y-%m-%d'), 'date_from': date_from.date().strftime('%Y-%m-%d')}


if __name__ == '__main__':
    pprint(insert_date())
