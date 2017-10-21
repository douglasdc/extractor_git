#coding:utf-8
from subprocess import PIPE, Popen
from sets import Set
import re, csv, json, logging

from scripts.run_shell import run_shell_scripts
from scripts.sh_scripts import *
from utils import *
from commit import Commit, Author
from metricas.find_your_library import library_expertise, expertise_distance
from metricas.expert_recomendation import depth_method, breadth_method, relative_breadth, relative_depth

commitsObj = {}
developers = {}
projects = {}
list_import_regex = []
list_api_methods = []
id_commit_method = {}

COMMIT_USER_METHOD = {}
AUTHOR_METHOD_RESUMO = {}
AUTHOR_METHOD_USE = {}

DEV_COMMIT = {}
DEV_METHOD = {}


def new_file_interest(path):
    return files_interest.append(path, git_path)

# Busca os commits que possuem referencia às expressões regulares de uma lista
def find_commits(list_regex, only_id=False, git_path=''):
    print 'Buscando commits pelos imports da API.....'

    list_regex = '|'.join(map(str, list_regex))
    result = []
    if only_id:
        ids = run_shell_scripts(commit_sha1_by_regex(list_regex, git_path), '')
        # print ids
        commits = strip_data_commit(ids)
        hash_commits = [y[0] for y in commits if len(y[0]) > 0]

        result = result + list(set(hash_commits))

    # print str(len(result)) + ' commits encontrados'
    info_file('output/commits_import.txt', result)
    return result

def get_commited_files(file_type, sh1a=None, git_path=''):
    if sh1a:
        return run_shell_scripts(commited_files(sh1a, file_type, git_path), '')
    else:
        return run_shell_scripts(see_changed_files(file_type, git_path), '')


# Busca arquivos que possuiram algum commit contendo refrencias a expressoes regulares presentes em uma lista
def get_interest_files(commits_sh1a, regex_list, git_path=''):
    files_interest = set()
    file = ''
    print 'Buscando arquivos de interesse dos commits.....'
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
    # print str(len(files_interest)) + ' arquivos de interesse encontrado'
    return files_interest

# Busca os commits que possuem referencia às expressões regulares em cada arquivo de uma lista de arquivos
# PRECISA AINDA VERIFICAR SE REALMENTE FAZ REFERENCIA A API, VERIFICAR SE A CLASSE OU MÉTODO É DA API
def commits_regex_by_file(regex_list, files, git_path=''):
    global commitsObj
    global developers
    # id_commit_method = {}
    print 'Buscando commits de arquivos pela lista de metodos.....'
    for file in files:
        for att in regex_list:
            
            commit_regex_file = []
            commit_hash = run_shell_scripts(commit_sha1_by_regex_file(att, file, git_path), '') #Hashs dos commits que usaram o atributo nesse arquivo
            commits = strip_data_commit(commit_hash)
            for commit in commits:
                if len(commit[0]) > 0:
                    if commit[0] not in id_commit_method:
                        id_commit_method[commit[0]] = []
                    
                    relation_dev_commit(commit, att, file, git_path)
                    # Insere a expressão na lista das expressoes alteradas por aquele commit
                    id_commit_method[commit[0]].append(att)
                    if commit[0] not in commitsObj:
                        c = Commit(commit[0], commit[1], commit[2], att, git_path, 0, 0)
                        commitsObj[commit[0]] = c
                    else:
                        commitsObj[commit[0]].insert_method(att, 0, 0)

                    if commit[1] not in developers:
                        a = Author(commit[1], att, 0, 0)
                        developers[commit[1]] = a
                    else:
                        developers[commit[1]].insert_method(att, 0, 0)

    info_file('output/commits_atributos.txt', id_commit_method)
    # print str(len(id_commit_method)) + ' commits encontrados'

def relation_dev_commit(commit, metodo, file, git_path):
    projeto = git_path.split('/')
    projeto = projeto[len(projeto) - 1]
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
        temp['projeto'] = projeto
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

    if (commit[1] not in AUTHOR_METHOD_RESUMO):
        temp = {}
        temp['desenvolvedor'] = commit[1]
        temp['metodos'] = set()
        temp['metodos'].add(metodo)
        temp['quantidade'] = 1
        temp['frequencia'] = count_insert
        AUTHOR_METHOD_RESUMO[commit[1]] = temp
    else:
        if metodo not in AUTHOR_METHOD_RESUMO[commit[1]]['metodos']:
            AUTHOR_METHOD_RESUMO[commit[1]]['quantidade'] = AUTHOR_METHOD_RESUMO[commit[1]]['quantidade'] + 1

        AUTHOR_METHOD_RESUMO[commit[1]]['metodos'].add(metodo)
        AUTHOR_METHOD_RESUMO[commit[1]]['frequencia'] = AUTHOR_METHOD_RESUMO[commit[1]]['frequencia'] + count_insert


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
            if insert:
                AUTHOR_METHOD_USE[commit[1]][metodo]['adicionou'] = AUTHOR_METHOD_USE[commit[1]][metodo]['adicionou'] + qtd
            else:
                AUTHOR_METHOD_USE[commit[1]][metodo]['removeu'] = AUTHOR_METHOD_USE[commit[1]][metodo]['removeu'] + qtd


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
        d['projeto'] = ''
        dict_writer = csv.DictWriter(output_file, fieldnames=d.keys(), extrasaction='ignore')
        dict_writer.writeheader()
        for data in COMMIT_USER_METHOD.values():
            for d in create_line_to_file(data):
                dict_writer.writerow(d)

    with open('output/tuplas_resumo.csv', 'w') as output_file:
        d = {}
        d['desenvolvedor'] = ''
        d['metodos'] = ''
        d['frequencia'] = ''
        d['quantidade'] = ''
        dict_writer = csv.DictWriter(output_file, fieldnames=d.keys(), extrasaction='ignore')
        dict_writer.writeheader()
        for data in AUTHOR_METHOD_RESUMO.values():
            d = {}
            d['desenvolvedor'] = data['desenvolvedor']
            d['metodos'] = ' | '.join(map(str, data['metodos']))
            d['frequencia'] = data['frequencia']
            d['quantidade'] = data['quantidade']
            dict_writer.writerow(d)

        
def create_line_to_file(commit_data):
    datas = []

    for key, value in commit_data['metodos'].iteritems():
        data = {}
        data['autor'] = commit_data['autor']
        data['commit_hash'] = commit_data['commit']
        data['timestamp'] = commit_data['timestamp']
        data['momento'] = commit_data['momento']
        data['metodo'] = key
        data['adicionado'] = value['adicionado']
        data['removido'] = value['removido']
        data['projeto'] = commit_data['projeto']
        datas.append(data)

    return datas


def load_files():
    global projects

    print 'Carregando parametros.....'
    try:
        parametros = open('parametros.json')
        parameters = json.load(parametros)
        projects = parameters['projetos']
    except Exception as ex:
        logging.critical('FALHA NO ARQUIVO DE PARAMETROS')
        print 'Verifique seu arquivo de parametros, algo de errado não está certo'


def load_imports():
    global list_import_regex

    print 'Carregando imports da API.....'
    file_imports = 'input/imports.txt'
    list_import_regex = get_list_lines_from_file(file_imports)

def load_methods():
    global list_api_methods

    print 'Carregando metodos da API.....'
    file_methods = 'input/metodos.txt'
    list_api_methods = get_list_lines_from_file(file_methods)

def find_your_library():
    print 'Calculando metricas do Find Your Library Experts.....'
    total = {}
    autor = {}
    for k, value in AUTHOR_METHOD_USE.iteritems():
        autor[k] = {key: value[key]['adicionou'] for key in value.keys()}
        for k2 in value.keys():
            total[k2] = max(total.get(k2, 0) + value[k2]['adicionou'], value[k2]['adicionou'])
    
    le = library_expertise(list_api_methods, autor)
    ed = expertise_distance(le)
    # print ed
    
    developers = []
    for dev, value in le.iteritems():
        temp = {}
        temp['exp_dist'] = ed[dev]
        temp['desenvolvedor'] = dev
        temp['lib_exp'] = value
        developers.append(temp)
        
    with open('output/find_your_library.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(
            output_file, fieldnames=developers[0].keys(), extrasaction='ignore')
        dict_writer.writeheader()
        for value in developers:
            dict_writer.writerow(value)


def expert_recomendation():
    print 'Calculand metricas do Expert Recommendation.....'
    total = {}
    autor = {}
    for k, value in AUTHOR_METHOD_USE.iteritems():
        autor[k] = {key: value[key]['adicionou'] for key in value.keys()}
        for k2 in value.keys():
            total[k2] = max(total.get(k2, 0) + value[k2]['adicionou'], value[k2]['adicionou'])

    dm = depth_method(autor)
    bm = breadth_method(autor)
    rd = relative_depth(total, autor)
    rb = relative_breadth(autor)

    developers = []
    for dev in dm.keys():
        temp = {}
        temp['depth'] = dm[dev]
        temp['breadth'] = bm[dev]
        temp['rel_depth'] = rd[dev]
        temp['rel_breadth'] = rb[dev]

        developers.append(temp)
    
    with open('output/expert_recommendation.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(
            output_file, fieldnames=developers[0].keys(), extrasaction='ignore')
        dict_writer.writeheader()
        for value in developers:
            dict_writer.writerow(value)

def start_extraction():
    print 'Iniciando.....'

    load_files()
    load_imports()
    load_methods()
    for project in projects:
        p = project.split('/')
        print 'Inicando extracao no projeto - '  + p[len(p) - 1]
        
        # Busca os commits que possuiram referencia aos imports
        commits_sh1a = find_commits(list_import_regex, True, project)
        
        # Busca os arquivos de interesse presentes no commits que possuiam referencia aos import dos 
        files_interest = get_interest_files(commits_sh1a,list_import_regex, project)

        # Extrai todos os commits que os arquivos de interesse tiveram, 
        # buscando os commits que possuem uso dos metodos presentes na lista
        commits_regex_by_file(list_api_methods, files_interest, project)

        out_cvs_tuple()

        find_your_library()

        expert_recomendation()
        # teste_create_out()
