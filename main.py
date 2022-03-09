import json
import shutil
import time
import datetime
import os
from progress.bar import IncrementalBar
import pickle
import pandas as pd
from shutil import rmtree

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
    config_file['last_file'] = last_file_name   # запись в конфиг название последнего файла в дирректории
    write_to_config_json(config_file)
    delta_time_format = datetime.datetime.strptime(last_file_name[-12:-4], '%Y%m%d') - datetime.timedelta(days=1095)
    delta_for_dumping = int(delta_time_format.strftime('%Y%m%d'))
    files_list_for_dump_new = []
    files_list_for_dump_new_csv = []
    files_list_for_search = []
    try:
        with open('dumped_files_list', 'rb') as f_obj:  # открывает файл со списком файлов которые были ранее упакованы
            files_list_dump_old = pickle.load(f_obj)
    except:
        files_list_dump_old = []

    for element in files_list:  # делит на два списка: то что отправится в дамп, и то что останется для поиска
        if int(element[-12:-4]) >= delta_for_dumping:
            files_list_for_search.append(element)
        else:
            files_list_for_dump_new.append(element)

    with open('files_list_for_search', 'wb') as f_obj:  # записывает файлы которые не в дампе, для поиска.
        pickle.dump(files_list_for_search, f_obj)

    with open('dumped_files_list', 'wb') as f_obj:  # записывает файл со списком того что в дампе
        pickle.dump(files_list_for_dump_new, f_obj)

    for element in files_list_dump_old:  # удаляет из списка файлов для дампа старые файл.
        files_list_for_dump_new.remove(element)

    for element in files_list_for_dump_new:  # создает список для дампа .csv
        files_list_for_dump_new_csv.append(element + '.csv')

    files_dict_for_dump = dict(zip(files_list_for_dump_new, files_list_for_dump_new_csv))

    os.makedirs('csv')

    for file_name in files_list_for_dump_new:  # парсит инфо файлов для дампа и упаковывает в dataframe csv
        with open('arp/' + file_name, 'r') as f_obj:
            readed_file = f_obj.readlines()
            new_read_file = []
            for element in readed_file:
                element = element.split(' ')[1:6:2]
                element.append(file_name[-12:-8])
                element.append(file_name.split('-')[0])
                new_read_file.append(element)
            df = pd.DataFrame(new_read_file, index=None)
            df.to_csv('csv/' + file_name + '.csv')

    try:  # open old concatinated file or create empty
        result = pd.read_csv('dumped_results.csv', index_col=0)
    except:
        result = pd.DataFrame()

    for key in files_dict_for_dump:
        print(f'Dumping the file: {key}')
        key = pd.read_csv('csv/' + files_dict_for_dump[key], index_col=0)
        concatinate_df = [result, key]
        result = pd.concat(concatinate_df, ignore_index=True)

    shutil.rmtree('csv')
    new_result = result.drop_duplicates()
    new_result.to_csv('dumped_results.csv')

    config_file['dumping'] = False  # dumping option OFF
    write_to_config_json(config_file)  # rewrite config file










if __name__ == "__main__":
    # user_data = input('Enter data to search: ')
    check_dumping()
    config = read_config_json()

    # in release delete: path='arp_short', arp_short
    directory_files_list = [file_name for file_name in os.listdir(path='arp') if
                            os.path.isfile(os.path.join('arp', file_name)) and '-ARP-' in file_name]
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
