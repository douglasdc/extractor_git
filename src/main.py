#coding:utf-8
from subprocess import PIPE, Popen
from scripts.run_shell import run_shell_scripts
from scripts.sh_scripts import *
from sets import Set
import re
import csv
import json
import logging

files_interest = set()
list_import_regex = []
list_api_methods = []
id_commit_method = {}

COMMIT_USER_METHOD = {}
AUTHOR_METHOD_USE = {}

DEV_COMMIT = {}
DEV_METHOD = {}

def strip_data_commit(commits):
    return [x.split('|') for x in commits.split('\n')]

def new_file_interest(path):
    return files_interest.append(path, git_path)

def get_list_lines_from_file(file_imports):
    linhas = None
    with open(file_imports) as f:
        linhas = f.readlines()

    return [x.strip() for x in linhas] 
# Busca os commits que possuem referencia às expressões regulares de uma lista

def info_file(file_path, data):
    with open(file_path, 'w') as f:
        if(type(data) is list):
            f.writelines('\n'.join(map(str, data)))
        elif(type(data) is dict):
            f.writelines('\n'.join(map(str, data)))
        else:
            f.write(data)

def find_commits(list_regex, only_id=False, git_path=''):
    print '.........BUSCANDO COMMITS.........'

    list_regex = '|'.join(map(str, list_regex))
    result = []
    if only_id:
        ids = run_shell_scripts(commit_sha1_by_regex(list_regex, git_path), '')
        # print ids
        commits = strip_data_commit(ids)
        hash_commits = [y[0] for y in commits if len(y[0]) > 0]

        result = result + list(set(hash_commits))

    print str(len(result)) + ' commits encontrados'
    info_file('output/commits_import.txt', result)
    return result

def get_commited_files(file_type, sh1a=None, git_path=''):
    if sh1a:
        return run_shell_scripts(commited_files(sh1a, file_type, git_path), '')
    else:
        return run_shell_scripts(see_changed_files(file_type, git_path), '')


# Busca arquivos que possuiram algum commit contendo refrencias a expressoes regulares presentes em uma lista
def get_interest_files(commits_sh1a, regex_list, git_path=''):
    file = ''
    print '.........BUSCANDO POR ARQUIVOS DE INTERESSE.........'
    try:
        for sh1a in commits_sh1a:
            if(len(sh1a) > 0):
                files = get_commited_files('java', sh1a, git_path)
                files = files.split('\n')
                for file_path in files:
                    if len(file_path) > 0 and file_path not in files_interest:
                        file = git_path + '/' + file_path
                        with open(git_path + '/' + file_path) as f:
                            for regex in regex_list:
                                if(re.search(regex, f.read())):
                                    # Insere os arquivos de cada commit na lista de arquivos de interesse
                                    files_interest.add(file_path)

    except Exception as e:
        logging.warning('Arquivo nao encontrato - ' + file)
    
    info_file('output/arquivos_interesse.txt', list(set(files_interest)))
    print str(len(files_interest)) + ' arquivos de interesse encontrado'


def count_metodos(commit_id, att, file, git_path):
    import string
    commit = run_shell_scripts(get_all_commit(commit_id, file, git_path), '')

    count_insert = 0
    count_remove = 0
    abs_metodo = 0
    for line in commit.split('\n'):
        if string.find(line, '+', 0, 1) != -1:
            count_insert = count_insert + len(re.findall('.info\(', line))
        
        if string.find(line, '-', 0, 1) != -1:
            count_remove = count_insert + len(re.findall('.info\(', line))

    print count_insert
    print count_remove

# Busca os commits que possuem referencia às expressões regulares em cada arquivo de uma lista de arquivos
# PRECISA AINDA VERIFICAR SE REALMENTE FAZ REFERENCIA A API, VERIFICAR SE A CLASSE OU MÉTODO É DA API
def commits_regex_by_file(regex_list, files, git_path=''):
    # id_commit_method = {}
    print '.........BUSCANDO COMMITS RELEVANTES NOS ARQUIVOS DE INTERESSE.........'
    for file in files:
        # print file
        for att in regex_list:
            
            commit_regex_file = []
            commit_hash = run_shell_scripts(commit_sha1_by_regex_file(att, file, git_path), '') #Hashs dos commits que usaram o atributo nesse arquivo
            commits = strip_data_commit(commit_hash)
            for commit in commits:
                if len(commit[0]) > 0:
                    if commit[0] not in id_commit_method:
                        id_commit_method[commit[0]] = []
                    
                    relation_dev_commit(commit, att, file, git_path)
                    # count_metodos(commit[0], att, file, git_path)
                    # Insere a expressão na lista das expressoes alteradas por aquele commit
                    id_commit_method[commit[0]].append(att)

    info_file('output/commits_atributos.txt', id_commit_method)
    print str(len(id_commit_method)) + ' commits encontrados'

# Novo desenvolvedor relacionado com o commit, metodos alterados (inseridos, removidos) no commit 
# e o momento em que o commit foi feito
def new_dev_commit(dev, commit, method, timestamp):
    # print '.........CRIANDO RELACAO DE DESENVOLVEDOR COM COMMIT.........'
    if dev not in DEV_COMMIT:
        DEV_COMMIT[dev] = []
    
    c = {}
    c['id'] = commit
    c['methods'] = method
    c['timestamp'] = timestamp

    DEV_COMMIT[dev].append(c)

    return DEV_COMMIT

# Novo desenvolvedor relacionado com o metodo, e quanto esse desenvolvedor tem usado o método
def new_dev_method(dev, method, qtd_uso):
    if dev not in DEV_METHOD:
        DEV_METHOD[dev] = {}

    if method not in DEV_METHOD[dev]:
        DEV_METHOD[dev][method] = 0
    
    DEV_METHOD[dev][method] = DEV_METHOD[dev][method] + 1

    return DEV_METHOD

def relation_dev_commit(commit, metodo, file, git_path):
    from datetime import datetime
    temp = {}
    temp_metodo = {}
    if(commit[0] not in COMMIT_USER_METHOD):
        temp = {}
        COMMIT_USER_METHOD[commit[0]] = temp
        temp['autor'] = commit[1]
        temp['timestamp'] = commit[2]
        temp['momento'] = "{:%d %b %Y %H:%M:%S}".format(datetime.fromtimestamp(float(commit[2])))
        temp['commit'] = commit[0]
        temp['metodos'] = {}
        temp['metodos'][metodo] = {}
    elif metodo not in COMMIT_USER_METHOD[commit[0]]['metodos']:
        COMMIT_USER_METHOD[commit[0]]['metodos'][metodo] = {}

    import string
    commit_all = run_shell_scripts(get_all_commit(commit[0], file, git_path), '')

    count_insert = 0
    count_remove = 0
    abs_metodo = 0
    for line in commit_all.split('\n'):
        if string.find(line, '+', 0, 1) != -1:
            count_insert = count_insert + len(re.findall('.' + metodo + '\(', line))
            count_commits(len(re.findall('.' + metodo + '\(', line)), commit, metodo, True)
        
        if string.find(line, '-', 0, 1) != -1:
            count_remove = count_insert + len(re.findall('.' + metodo + '\(', line))
            count_commits(len(re.findall('.' + metodo + '\(', line)), commit, metodo, False)

    COMMIT_USER_METHOD[commit[0]]['metodos'][metodo]['adicionado'] = count_insert
    COMMIT_USER_METHOD[commit[0]]['metodos'][metodo]['removido'] = count_remove

    # print COMMIT_USER_METHOD
        # temp['metodo'] = metodo
        # temp['quantidade'] = DEV_METHOD[autor][metodo]

def count_commits(qtd, commit, metodo, insert=True):
    if(commit[1] not in AUTHOR_METHOD_USE):
        AUTHOR_METHOD_USE[commit[1]] = {}
        AUTHOR_METHOD_USE[commit[1]][metodo] = {'adicionou':0, 'removeu':0}
        if insert:
            AUTHOR_METHOD_USE[commit[1]][metodo]['adicionou'] = qtd
        else:
            AUTHOR_METHOD_USE[commit[1]][metodo]['removeu'] = qtd
    else:
        if (metodo not in AUTHOR_METHOD_USE[commit[1]]):
            AUTHOR_METHOD_USE[commit[1]][metodo] = {'adicionou':0, 'removeu':0}
            if insert:
                AUTHOR_METHOD_USE[commit[1]][metodo]['adicionou'] = qtd
            else:
                AUTHOR_METHOD_USE[commit[1]][metodo]['removeu'] = qtd
        else:
            # AUTHOR_METHOD_USE[commit[1]][metodo] = AUTHOR_METHOD_USE[commit[1]][metodo] + 1
            if insert:
                AUTHOR_METHOD_USE[commit[1]][metodo]['adicionou'] = AUTHOR_METHOD_USE[commit[1]][metodo]['adicionou'] + qtd
            else:
                AUTHOR_METHOD_USE[commit[1]][metodo]['removeu'] = AUTHOR_METHOD_USE[commit[1]][metodo]['removeu'] + qtd

# Extrai as informações do commit, autor, timestamp(UNIX)
def extract_info_commit(id_commit, git_path=''):
    # for id in id_commit:
    author = run_shell_scripts(author_commit_sha1(id_commit, git_path), '').replace('\n', '')
    timestamp = run_shell_scripts(timestamp_commit_sha1(id_commit, git_path), '').replace('\n', '')
    methods = []
    new_dev_commit(author, id_commit, id_commit_method[id_commit], timestamp )
    for method in id_commit_method[id_commit]:
        new_dev_method(author, method, 1)

def out_cvs_tuple():
    with open('output/tuplas_extraidas.csv', 'w') as output_file:
        d = {}
        d['autor'] = ''
        d['commit_hash'] = ''
        d['timestamp'] = ''
        d['momento'] = ''
        d['metodo'] = ''
        d['adicionado'] = ''
        d['removido'] = ''
        dict_writer = csv.DictWriter(output_file, fieldnames=d.keys(), extrasaction='ignore')
        dict_writer.writeheader()
        for data in COMMIT_USER_METHOD.values():
            for d in create_line_to_file(data):
                # print '\n'
                # print d
                dict_writer.writerow(d)
            # print create_line_to_file(data)

    # print COMMIT_USER_METHOD
        
def create_line_to_file(commit_data):
    datas = []

    # print commit_data['metodos']
    for key, value in commit_data['metodos'].iteritems():
        data = {}
        data['autor'] = commit_data['autor']
        data['commit_hash'] = commit_data['commit']
        data['timestamp'] = commit_data['timestamp']
        data['momento'] = commit_data['momento']
        data['metodo'] = key
        data['adicionado'] = value['adicionado']
        data['removido'] = value['removido']
        # print data
        datas.append(data)

    return datas

# print run_shell_scripts(all_contribuitors_name, '')
def primeiro():
    print 'COMEÇANDO EXTRAÇÃO DAS INFORMAÇÕES'

    try:
        parametros = open('parametros.json')
        parameters = json.load(parametros)
        projects = parameters['projetos']
    except Exception as ex:
        logging.critical('FALHA NO ARQUIVO DE PARAMETROS')
        print 'Verifique seu arquivo de parametros, algo de errado não está certo'
        
    for project in projects:
        print '\n\n===== Buscando no projeto '  + project + ' ====='
        file_imports = 'input/imports.txt' # Arquivo com padrões do import da api desejada
        
        # Arquivo com os padrões das chamadas de métodos
        file_methods = 'input/metodos.txt'
        list_import_regex = get_list_lines_from_file(file_imports) # Converte o arquivo em lista
        list_api_methods = get_list_lines_from_file(file_methods) # Converte o arquivo em lista
        
        # Busca os commits que possuiram referencia aos imports
        commits_sh1a = find_commits(list_import_regex, True, project)
        
        # Busca os arquivos de interesse presentes no commits que possuiam referencia aos import dos 
        get_interest_files(commits_sh1a,list_import_regex, project)

        # Extrai todos os commits que os arquivos de interesse tiveram, 
        # buscando os commits que possuem uso dos metodos presentes na lista
        # get_commits_regex_by_file(list_api_methods, files_interest, project)
        commits_regex_by_file(list_api_methods, files_interest, project)

        # print id_commit_method
        # for commit in id_commit_method:
        #     extract_info_commit(commit, project)

        out_cvs_tuple()
        # out_dev_data(list_api_methods)

