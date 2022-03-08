import os.path
import numpy as np
import pandas as pd
import time
import threading
import datetime
import pickle


def counting_thread(splited_list, name_file):
    for item in splited_list:
        print(f'searching {user_answer} in {item}')
        with open(item) as f_obj:
            data_list = f_obj.readlines()
        matching = [s for s in data_list if user_answer in s]
        with open(name_file, 'a', encoding='utf-8') as f:
            if len(matching) >= 1:
                f.write(f'{item}\n')
            for line_element in matching:
                f.write(f'{line_element}')



with open('last_time_check') as f_obj:
    last_time_check = f_obj.read()
actual_date = datetime.datetime.now().strftime('%Y%m%d')

if int(actual_date) > int(last_time_check):
    with open('last_time_check', 'w') as f_obj:
        f_obj.write(actual_date)

directory_list = [file_name for file_name in os.listdir() if
                  os.path.isfile(os.path.join('', file_name)) and '-ARP-' in file_name]
directory_list.sort(key=lambda x: int(x[-12:-4]))

directory_list_cut, directory_list_dump_new, directory_list_for_dump, csv_directory_for_dump = [], [], [], []

past_date = datetime.datetime.strptime((directory_list[-1])[-12:-4], '%Y%m%d') - datetime.timedelta(days=1095)
dt_string = int(past_date.strftime('%Y%m%d'))

try:
    with open('directory_list_dump_old', 'rb') as f_obj:
        directory_list_dump_old = pickle.load(f_obj)
except:
    directory_list_dump_old = []

for element in directory_list:
    if int(element[-12:-4]) >= dt_string:
        directory_list_cut.append(element)
    else:
        directory_list_dump_new.append(element)

for element in directory_list_dump_new:
    if element not in directory_list_dump_old:
        directory_list_for_dump.append(element)

with open('directory_list_dump_old', 'wb') as f_obj:
    pickle.dump(directory_list_dump_new, f_obj)

for element in directory_list_for_dump:
    csv_directory_for_dump.append(element + '.csv')

directory_dict_for_dump = dict(zip(directory_list_for_dump, csv_directory_for_dump))

for file_name in directory_list_for_dump:
    with open(file_name, 'r') as f_obj:
        readed_file = f_obj.readlines()
        new_read_file = []
        for element in readed_file:
            element = element.split(' ')[1:6:2]
            element.append(file_name[-12:-8])
            element.append(file_name.split('-')[0])
            new_read_file.append(element)
        df = pd.DataFrame(new_read_file, index=None)
        df.to_csv(file_name + '.csv')

try:
    result = pd.read_csv('dump_result.csv', index_col=0)
except:
    result = pd.DataFrame()
for key in directory_dict_for_dump:
    print(f'Dumping the file: {key}')
    key = pd.read_csv(directory_dict_for_dump[key], index_col=0)
    concatinate_df = [result, key]
    result = pd.concat(concatinate_df, ignore_index=True)

for el in csv_directory_for_dump:
    os.remove(el)

new_result = result.drop_duplicates()
new_result.to_csv('dump_result.csv')

try:
    os.remove('aresult.csv')
except:
    pass

user_answer = input('Enter data for search: ')
thread_numbers = 32

names_threads = []

for element in range(thread_numbers):
    names_threads.append(f'thread_{element}')  # names_threads = ['thread_0', 'thread_1' ....]

split_list = np.array_split(directory_list_cut, thread_numbers)
my_dict = {names_threads[idx]: split_list[idx] for idx, el in enumerate(names_threads)}

thread_list = []

dump_thread_list = ['dump_result.csv']
dump_thread = threading.Thread(target=counting_thread, name='dump_thread',
                               args=(dump_thread_list, 'dump_thread_result'))
dump_thread.start()

for i in range(thread_numbers):
    t = threading.Thread(target=counting_thread, name=names_threads[i],
                         args=(my_dict.get(names_threads[i]), names_threads[i]))
    thread_list.append(t)
    t.start()

dump_thread.join()

for el in thread_list:
    el.join()

with open("result.txt", "w") as out_file:
    with open('dump_thread_result') as f_obj:
        out_file.write(f_obj.read())
    for f in names_threads:
        with open(f, "r") as in_file:
            print(f'Collecting the file: {f}')
            out_file.write(in_file.read())

# with open('result.txt') as f_obj:
# print(f_obj.read())

for delete_files in names_threads:
    os.remove(delete_files)
os.remove('dump_thread_result')

print(input('Enter for exit...'))
os.system('notepad.exe ' + 'result.txt')
