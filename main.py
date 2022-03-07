import json
import time
import datetime
from progress.bar import IncrementalBar


def check_dumping():
    """Checking if program dumping new data, with progress bar"""
    while True:
        with open('config.json', 'r') as json_obj:
            config_temp = json.load(json_obj)
            if not config_temp['dumping']:
                break
            bar = IncrementalBar('Database dumping. Please wait', max=10)
            for item in range(10):
                bar.next()
                time.sleep(1)
            bar.finish()


"""if __name__ == "__main__":
    user_data = input('Enter data to search: ')
    check_dumping()"""

with open('config.json', 'r') as json_obj:
    config = json.load(json_obj)
actual_date = datetime.datetime.now().strftime('%Y%m%d')
config['last_time_check'] = int(actual_date)
print(config['last_time_check'])
print(config)

with open('config.json', 'w') as json_obj:
    json.dump(config, json_obj)
