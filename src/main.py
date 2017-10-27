#coding:utf-8
from subprocess import PIPE, Popen
from sets import Set
import re, csv, json, logging
import timeit

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


def new_file_interest(path):
    return files_interest.append(path, git_path)

# Busca os commits que possuem referencia às expressões regulares de uma lista
def find_commits(list_regex, only_id=False, git_path=''):
    print 'Buscando commits pelos imports da API.....'

    list_regex = '|'.join(map(str, list_regex))
    result = []
    if only_id:
        ids = run_shell_scripts(commit_sha1_by_regex(list_regex, git_path), '')
        commits = strip_data_commit(ids)
        hash_commits = [y[0] for y in commits if len(y[0]) > 0]

        result = result + list(set(hash_commits))

    info_file('output/commits_import.txt', result)
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
    try:
        for sh1a in commits_sh1a:
            if(len(sh1a) > 0):
                files = get_commited_files(LINGUAGENS, sh1a, git_path)
                files_interest = files_interest + [git_path + '/' + file for file in files.split('\n') if len(file) > 0]

    except Exception as e:
        logging.warning('Arquivo nao encontrato - ' + file)
    
    info_file('output/arquivos_interesse.txt', list(set(files_interest)))
    return list(set(files_interest))

# Busca os commits que possuem referencia às expressões regulares em cada arquivo de uma lista de arquivos
# PRECISA AINDA VERIFICAR SE REALMENTE FAZ REFERENCIA A API, VERIFICAR SE A CLASSE OU MÉTODO É DA API
def commits_regex_by_file(regex_list, files, git_path=''):
    global commitsObj
    global developers
    commits2 = {}

    print 'Buscando commits de arquivos pela lista de metodos.....'
    tat = '\(|.'.join(map(str, regex_list))
    for file in files:
        #Hashs dos commits que usaram o atributo nesse arquivo
        commit_hash = run_shell_scripts(commit_sha1_by_regex_file(tat, file, git_path), '') 

        if len(commit_hash) > 0:
            commits = strip_data_commit(commit_hash)
            for commit in commits:

                if commit[0] not in id_commit_method:
                    id_commit_method[commit[0]] = []

                if commit[0] not in commits:
                    temp = {}
                    temp['commit'] = commit[0]
                    temp['autor'] = commit[1]
                    temp['timestamp'] = commit[2]
                    temp['metodos'] = []
                    temp['arquivos'] = []
                    temp['arquivos'].append(file)

                    commits2[commit[0]] = temp
                else:
                    commits2[commit[0]]['arquivos'].append(file)

    info_file('output/commits_atributos.txt', id_commit_method)
    return commits2


def load_files():
    global projects
    global PROJETOS
    global CONSIDERAR_REMOCAO
    global LINGUAGENS

    print 'Carregando parametros.....'
    try:
        parametros = open('parametros.json')
        parameters = json.load(parametros)
        projects = parameters['projetos']
        PROJETOS = projects
        CONSIDERAR_REMOCAO = parameters['considerar_removidos']

        if parameters['code_java']: LINGUAGENS.append('java')
        if parameters['code_python']: LINGUAGENS.append('py')
        if parameters['code_javascript']: LINGUAGENS.append('js')
        if parameters['code_php']: LINGUAGENS.append('php')

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

def find_your_library(commits):
    
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

def start_extraction():
    print 'Iniciando.....'

    global PROJETO_ATUAL

    load_files()
    load_imports()
    load_methods()
    for project in projects:
        p = project.split('/')
        PROJETO_ATUAL = p
        print 'Inicando extracao no projeto - '  + p[len(p) - 1]
        
        # Busca os commits que possuiram referencia aos imports
        commits_sh1a = find_commits(list_import_regex, True, project)
        
        # Busca os arquivos de interesse presentes no commits que possuiam referencia aos import dos 
        files_interest = get_interest_files(commits_sh1a, list_import_regex, project)

        # Extrai todos os commits que os arquivos de interesse tiveram, 
        # buscando os commits que possuem uso dos metodos presentes na lista
        # commits = commits_regex_by_file(list_api_methods, files_interest, project)
        commits = commits_regex_by_file(list_api_methods, files_interest, project)

        for key, value in commits.iteritems():
            commit_all = ''
            for file in value['arquivos']:
                commit_all = run_shell_scripts(get_all_commit(key, file, project), '')
                # print commit_all
            contagem = find_patters_commit(commit_all, list_api_methods, CONSIDERAR_REMOCAO)
            value['metodos'] = contagem

        general = summary(commits)
        s_author = summary_author(commits)

        tuplas_geral(general)
        tuplas_resumo(s_author)

        find_your_library(s_author)
        expert_recomendation(s_author)
