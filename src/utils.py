#coding:utf-8

def strip_data_commit(commits):
    return [x.split('|') for x in commits.split('\n')]


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
