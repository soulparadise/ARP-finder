import json
import time
import datetime
import os
from progress.bar import IncrementalBar
import pickle


def check_dumping():
    """Checking if program dumping new data, with progress bar"""
    while True:
        config_temp = read_config_json()
        if not config_temp['dumping']:
            break
        progress_bar = IncrementalBar('Database dumping. Please wait', max=10)
        for _ in range(10):
            progress_bar.next()
            time.sleep(1)
        progress_bar.finish()


def write_to_config_json(config_input):
    """writing config to config.json"""
    with open('config.json', 'w', encoding='UTF-8') as json_obj:
        json.dump(config_input, json_obj)


def read_config_json():
    """return config from file: config.json"""
    with open('config.json', 'r', encoding='UTF-8') as json_obj:
        config = json.load(json_obj)
    return config


def dumping(files_list, config_file):
    config_file['dumping'] = True  # dumping option ON
    last_file_name = files_list[-1]
    config_file['last_file'] = last_file_name
    write_to_config_json(config_file)
    print(config_file)


if __name__ == "__main__":
    # user_data = input('Enter data to search: ')
    # check_dumping()
    config = read_config_json()

    # in release delete: path='arp_short', arp_short
    directory_files_list = [file_name for file_name in os.listdir(path='arp_short') if
                            os.path.isfile(os.path.join('arp_short', file_name)) and '-ARP-' in file_name]
    directory_files_list.sort(key=lambda x: int(x[-12:-4]))

    if config['last_file'] == directory_files_list[-1]:
        # выполняется поиск
        print('search')
    else:
        # выполняется dumping
        dumping(directory_files_list, config)

    # delta_date_full = datetime.datetime.strptime((directory_files_list[-1])[-12:-4], '%Y%m%d') - datetime.timedelta(
    #     days=1095)
    # delta_date = int(delta_date_full.strftime('%Y%m%d'))
    # try:
    #     with open('directory_list_dump_old', 'rb') as f_obj:
    #         directory_list_dump_old = pickle.load(f_obj)
    # except:
    #     directory_list_dump_old = []
