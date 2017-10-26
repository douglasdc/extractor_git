#coding:utf-8
import csv

def strip_data_commit(commits):
    return [commit.split('|') for commit in commits.split('\n')]


def get_list_lines_from_file(file_imports):
    linhas = None
    with open(file_imports) as f:
        linhas = f.readlines()

    return [x.strip() for x in linhas]


def info_file(file_path, data):
    with open(file_path, 'w') as f:
        if(type(data) is list):
            f.writelines('\n'.join(map(str, data)))
        elif(type(data) is dict):
            f.writelines('\n'.join(map(str, data)))
        else:
            f.write(data)


def write_csv(out_path, file_name, out_dict):
    with open(out_path + '/' + file_name + '.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(
            output_file, fieldnames=out_dict[0].keys(), extrasaction='ignore')
        dict_writer.writeheader()
        for value in out_dict:
            dict_writer.writerow(value)
