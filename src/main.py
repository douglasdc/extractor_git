#coding:utf-8
from subprocess import PIPE, Popen
from sets import Set
import re, csv, json, logging
import timeit
import time

from scripts.run_shell import run_shell_scripts
from scripts.sh_scripts import *
from utils import *
from commit import Commit, Author
from metricas.find_your_library import library_expertise, expertise_distance
from metricas.expert_recomendation import depth_method, breadth_method, relative_breadth, relative_depth
from parser import *
from data import *
from data_export import *
from parametros import *

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
SINCE = ''
UNTIL = ''

def new_file_interest(path):
    return files_interest.append(path, git_path)

# Busca os commits que possuem referencia às expressões regulares de uma lista
def find_commits(list_regex, only_id=False, git_path=''):
    print 'Buscando commits pelos imports da API.....'

    list_regex = '|'.join(map(str, list_regex))
    result = []
    if only_id:
        ids = run_shell_scripts(commit_sha1_by_regex(list_regex, git_path, SINCE, UNTIL), '')
        commits = strip_data_commit(ids)
        hash_commits = [y[0] for y in commits if len(y[0]) > 0]

        result = result + list(set(hash_commits))

    info_file('output/commits_import.txt', result)
    print 'Encontrado ' + str(len(result)) + ' commits'
    return result


def get_commited_files(file_type, sh1a=None, git_path=''):
    if sh1a:
        return run_shell_scripts(commited_files(sh1a, file_type, git_path), '')
    else:
        return run_shell_scripts(see_changed_files(file_type, git_path), '')


# Busca arquivos que possuiram algum commit contendo refrencias a expressoes regulares presentes em uma lista
def get_interest_files(commits_sh1a, regex_list, git_path=''):
    files_interest = []
    file = ''
    print 'Buscando arquivos de interesse dos commits.....'
    startTime = int(round(time.time() * 1000))
    regex = '|'.join(map(str, list_import_regex))
    try:
        for sh1a in commits_sh1a:
            if(len(sh1a) > 0):
                full_path = git_path + '/' + file

                files = run_shell_scripts('git -C ' + git_path + ' show --pretty="" -G' + '"' + regex + '"' + ' --no-commit-id --name-only -r ' + sh1a, '')
                files_interest = files_interest + [git_path + '/' + file for file in files.split('\n') if git_path + '/' + file not in files_interest and len(file) > 0 and
                    len(run_shell_scripts('[ ! -f "' + git_path + '/' + file + '" ] && echo "Arquivo existe"', '')) > 0]

    except Exception as e:
        logging.warning('Arquivo nao encontrato - ' + file)
    endTime = int(round(time.time() * 1000))
    # info_file('output/arquivos_interesse.txt', list(set(files_interest)))
    print 'Encontrato ' + str(len(files_interest)) + ' arquivos'
    return list(set(files_interest))

# Busca os commits que possuem referencia às expressões regulares em cada arquivo de uma lista de arquivos
# PRECISA AINDA VERIFICAR SE REALMENTE FAZ REFERENCIA A API, VERIFICAR SE A CLASSE OU MÉTODO É DA API
def commits_regex_by_file(regex_list, files, git_path=''):
    import progressbar
    barA = progressbar.ProgressBar()
    barM = progressbar.ProgressBar(max_value=len(files), redirect_stdout=True)
    global commitsObj
    global developers
    commits2 = {}

    print 'Buscando commits de arquivos pela lista de metodos.....'
    tat = '\(|.'.join(map(str, regex_list))
    i = 0
    j = 0
    for file in files:
        i = i + 1
        k = 100*i/len(files)
        # barA.update(k)
        #Hashs dos commits que usaram o atributo nesse arquivo
        # print i
        # for tat in regex_list:
        j = j + 1
        barM.update(j)
        # print str(i) + '/43' + '-----' + str(j)
        commit_hash = run_shell_scripts(commit_sha1_by_regex_file(tat, file, git_path, SINCE, UNTIL), '')
        # print commit_hash
        if len(commit_hash) > 0:
            commits = strip_data_commit(commit_hash)
            for commit in commits:

                if commit[0] not in id_commit_method:
                    id_commit_method[commit[0]] = []

                if commit[0] not in commits:
                    temp = {}
                    temp['commit'] = commit[0]
                    if 'Maurício' in commit[1] or 'Mauricio' in commit[1]:
                        temp['autor'] = 'Mauricio'
                    elif 'Barry' in commit[1] or 'bcron10' in commit[1]:
                        temp['autor'] = 'Barry Cronin'
                    else:
                        temp['autor'] = commit[1]
                    temp['timestamp'] = commit[2]
                    temp['email'] = commit[3]
                    temp['metodos'] = []
                    temp['arquivos'] = []
                    temp['arquivos'].append(file)

                    commits2[commit[0]] = temp
                else:
                    commits2[commit[0]]['arquivos'].append(file)

    info_file('output/commits_atributos.txt', id_commit_method)
    print 'Encontrato ' + str(len(commits2)) + ' commits'
    return commits2


def load_files():
    from datetime import datetime
    global projects
    global PROJETOS
    global CONSIDERAR_REMOCAO
    global LINGUAGENS
    global REMOVER_LINHAS_IDENTICAS
    global SINCE
    global UNTIL

    print 'Carregando parametros.....'
    try:
        parametros = open('parametros.json')
        parameters = json.load(parametros)
        projects = parameters['projetos']
        PROJETOS = projects
        CONSIDERAR_REMOCAO = parameters['considerar_removidos']
        REMOVER_LINHAS_IDENTICAS = parameters['linhas_identicas']

        if parameters['code_java']: LINGUAGENS.append('java')
        if parameters['code_python']: LINGUAGENS.append('py')
        if parameters['code_javascript']: LINGUAGENS.append('js')
        if parameters['code_php']: LINGUAGENS.append('php')

        SINCE = datetime.strptime(parameters['data_inicio'], "%Y-%m-%d").date()
        UNTIL = datetime.strptime(parameters['data_fim'], "%Y-%m-%d").date()

    except Exception as ex:
        logging.critical('FALHA NO ARQUIVO DE PARAMETROS')
        print 'Verifique seu arquivo de parametros, algo de errado não está certo'


def load_imports():
    global list_import_regex

    print 'Carregando imports da API.....'
    file_imports = 'input/imports.txt'
    list_import_regex = get_list_lines_from_file(file_imports)
    # print list_import_regex
    print 'Imports no arquivo: ' + str(len(list_import_regex))


def load_methods():
    global list_api_methods

    print 'Carregando metodos da API.....'
    file_methods = 'input/metodos_log4j.txt'
    list_api_methods = get_list_lines_from_file(file_methods)
    # print list_api_methods
    print 'Metodos no arquivo: ' + str(len(list_api_methods))


def find_your_library(commits):
    print 'Calculando metricas do Find Your Library.....'
    
    autor = autor_methods_frequency(commits, CONSIDERAR_REMOCAO)
    # total = methods_total_frequency(commits)
    le = library_expertise(list_api_methods, autor)
    ed = expertise_distance(le)
    find_libray__csv(le, ed)
    

def expert_recomendation(commits):
    print 'Calculando metricas do Expert Recommendation.....'
    autor = autor_methods_frequency(commits, CONSIDERAR_REMOCAO)

    dm = depth_method(autor)
    bm = breadth_method(autor)
    rd = relative_depth(autor)
    rb = relative_breadth(autor)

    expertise__csv(dm, bm, rd, rb)


def count_commits(commits, project):
    commits = commits.copy()
    for key, value in commits.iteritems():
        commit_all = ''
        for file in value['arquivos']:
            commit_all = run_shell_scripts(get_all_commit(key, file, project), '')

        contagem = find_patters_commit(commit_all, list_api_methods, CONSIDERAR_REMOCAO)
        commits[key]['metodos'] = contagem
    return commits


def start_extraction():
    print 'Iniciando.....'

    global PROJETO_ATUAL

    load_files()
    load_imports()
    load_methods()
    general = {}
    s_author = {}
    all_files_interest = []
    for project in projects:
        p = project.split('/')
        PROJETO_ATUAL = p[len(p) - 1]
        print 'Inicando extracao no projeto - '  + p[len(p) - 1]
        
        # Busca os commits que possuiram referencia aos imports
        commits_sh1a = find_commits(list_import_regex, True, project)
        
        # Busca os arquivos de interesse presentes no commits que possuiam referencia aos import dos 
        files_project = get_interest_files(commits_sh1a, list_import_regex, project)
        all_files_interest = all_files_interest + files_project

        # Extrai todos os commits que os arquivos de interesse tiveram, 
        # buscando os commits que possuem uso dos metodos presentes na lista
        # commits = commits_regex_by_file(list_api_methods, files_interest, project)
        commits = commits_regex_by_file(list_api_methods, files_project, project)
        
        commits = count_commits(commits, project)

        general.update(summary(commits))
        s_author.update(summary_author(commits))

        # list_regex = '\(|.'.join(map(str, list_api_methods))
        
        # for file in files_project:
        #     file_path = project + '/' + file
        #     m = '|'.join(map(str, list_api_methods))
        #     # a = commits_regex_by_file(list_api_methods, files_project, project)
        #     commit_hash = run_shell_scripts(get_amount_commits(m, file, project, SINCE, UNTIL), '')
        #     # print commit_hash
        #     # print a

    try:
        tuplas_geral(general)
        tuplas_resumo(s_author)
        find_your_library(s_author)
        expert_recomendation(s_author)
    except Exception as e:
        logging.warning('0 Commits encontrados no projeto, verifique os parâmetros e api que desejam buscar')
        print '0 Commits encontratos no projeto, verifique os parâmetros e api que desejam buscar'
