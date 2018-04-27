import requests
import pytz
from datetime import datetime


def get_attempt_data(url, payload=()):
    return requests.get(url, params=payload).json()


def load_attempts(url):
    payload = {'page': 1}
    page_data = get_attempt_data(url, payload)
    n_pages = page_data['number_of_pages']
    while True:
        if payload['page'] <= n_pages:
            page_data = get_attempt_data(url, payload)
            n_pages = page_data['number_of_pages']
            for record in page_data['records']:
                yield {
                    'username': record['username'],
                    'timestamp': record['timestamp'],
                    'timezone': record['timezone'],
                    }
            payload['page'] += 1
        else:
            break


def get_attempt_hour(time_zone, timestamp):
    local_tz = pytz.timezone(time_zone)
    date_time = datetime.fromtimestamp(timestamp, local_tz)
    return date_time.hour


def get_midnighters(loaded_attempts):
    start_hour = 0
    end_hour = 6
    for attempt in loaded_attempts:
        hour = get_attempt_hour(attempt['timezone'], attempt['timestamp'])
        if start_hour <= hour <= end_hour:
            yield attempt


def get_uniq_midnighters(midnighters_data):
    uniq_midnighters = []
    for midnighter in midnighters_data:
        uniq_midnighters.append(midnighter['username'])
    return sorted(list(set(uniq_midnighters)))


def print_midnighters(midnighters_data):
    print('Midnighters are:')
    for midnighter in midnighters_data:
        print('\t*', midnighter)


if __name__ == '__main__':
    url = 'http://devman.org/api/challenges/solution_attempts/'
    loaded_attempts = load_attempts(url)
    midnighters_data = get_midnighters(loaded_attempts)
    unique_midnighters = get_uniq_midnighters(midnighters_data)
    print_midnighters(unique_midnighters)
