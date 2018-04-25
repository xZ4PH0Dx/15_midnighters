import requests
import pytz
from datetime import datetime


def get_json(url):
    return requests.get(url).json()


def load_attempts(pages, url):
    for page in range(1, pages+1):
        data_on_page = get_json(url+str(page))
        for record in data_on_page['records']:
            yield {
                'username': record['username'],
                'timestamp': record['timestamp'],
                'timezone': record['timezone'],
                }


def get_hour(time_zone, timestamp):
    local_tz = pytz.timezone(time_zone)
    date_time = datetime.fromtimestamp(timestamp, local_tz)
    return date_time.hour


def get_midnighters(loaded_attempts):
    midnight_hours = (0, 1, 2,)
    for attempt in loaded_attempts:
        hour = get_hour(attempt['timezone'], attempt['timestamp'])
        if hour in midnight_hours:
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
    url = 'http://devman.org/api/challenges/solution_attempts/?page='
    loaded_first_page = get_json(url+'1')
    n_pages = loaded_first_page['number_of_pages']
    loaded_attempts = load_attempts(n_pages, url)
    midnighters_data = get_midnighters(loaded_attempts)
    unique_midnighters = get_uniq_midnighters(midnighters_data)
    print_midnighters(unique_midnighters)
