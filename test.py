files_list_for_dump_new = ['q', 'w', 'e', 'r', 't']
files_list_dump_old = ['q', 'w', 'e']

for el in files_list_for_dump_new.copy():
    if el in files_list_dump_old:
        files_list_for_dump_new.remove(el)


print(files_list_for_dump_new)
