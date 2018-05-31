#coding:utf-8
import csv
import logging

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
    if len(out_dict) > 0:
        with open(out_path + '/' + file_name + '.csv', 'w', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(
                output_file, fieldnames=out_dict[0].keys(), extrasaction='ignore')
            dict_writer.writeheader()
            for value in out_dict:
                try:
                    dict_writer.writerow(value)
                except Exception as e:
                    logging.info('Erro ao escrever a linha >> ' + value)
                    print("Erro ao escrever linha no arquivo " + file_name + "csv")
                    
    else:
        print("Nenhum dado para escrever no arquivo")


def split_list(itens, parts):
    avg = len(itens) / float(parts)
    out = []
    last = 0.0

    while last < len(itens):
        out.append(itens[int(last):int(last + avg)])
        last += avg

    return out