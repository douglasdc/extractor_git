#!/usr/bin/env python3
#coding:utf-8
from subprocess import PIPE, Popen
# from sets import Set
import re, csv, json, logging, timeit, time, os, threading
from multiprocessing import Manager, Process, cpu_count, Value
from datetime import timedelta

from .scripts.run_shell import run_shell_scripts
from .scripts.sh_scripts import *
from .utils import *
from .metricas.find_your_library import library_expertise, expertise_distance
from .metricas.expert_recomendation import depth_method, breadth_method, relative_breadth, relative_depth
from .parser import *
from .data import *
from .data_export import *
from .models import Author, Commit, Method, File
from .oraculo import oraculo_david_ma
from . import settings

manager = Manager()

# Busca os commits que possuem referencia às expressões regulares de uma lista
o = 0
def find_commits(list_regex, since, until, only_id=False, git_path=''):
    print('Buscando commits pelos imports da API.....')

    list_regex = '|'.join(map(str, list_regex))

    result = []
    if only_id:
        ids = run_shell_scripts(commit_sha1_by_regex(list_regex, git_path, since, until), '')
        commits = strip_data_commit(ids)
        hash_commits = [y[0] for y in commits if len(y[0]) > 0]

        result = result + list(set(hash_commits))

    info_file('output/commits_import.txt', result)
    print('Encontrado ' + str(len(result)) + ' commits')

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
    print('Buscando arquivos de interesse dos commits.....')
    startTime = int(round(time.time() * 1000))
    regex = '|'.join(map(str, settings.LIST_IMPORT_REGEX))
    
    try:
        for sh1a in commits_sh1a:
            if(len(sh1a) > 0):
                full_path = git_path + '/' + file

                # files = run_shell_scripts('git -C ' + git_path + ' show --pretty="" -G' + '"' + regex + '"' + ' --no-commit-id --name-only -r ' + sh1a, '')
                files = run_shell_scripts(get_all_files(git_path, regex, sh1a), '')
                files_interest = files_interest + [git_path + '/' + file for file in files.split('\n') if git_path + '/' + file not in files_interest and len(file) > 0 and
                    len(run_shell_scripts(search_for_single_file(git_path, file), '')) > 0]

    except Exception as e:
        print(e)
        logging.warning('Arquivo nao encontrato - ' + file)
    endTime = int(round(time.time() * 1000))
    # info_file('output/arquivos_interesse.txt', list(set(files_interest)))
    print('Encontrato ' + str(len(files_interest)) + ' arquivos')
    return list(set(files_interest))


def extract_commits_regex_by_file(files, regex_list, since, until, autores, git_path=''):

    import progressbar
    # barA = progressbar.ProgressBar()
    # barM = progressbar.ProgressBar(max_value=len(files), redirect_stdout=True)

    tat = '\(|.'.join(map(str, regex_list))
    j = 0
    mf = []
    for file in files:
        j = j + 1
        # barM.update(j)
        commit_hash = run_shell_scripts(commit_sha1_by_regex_file(tat, file, git_path, since, until), '')

        if len(commit_hash) > 0:
            commits = strip_data_commit(commit_hash)
            
            for commit in commits:
                nc = Commit(commit[0], commit[2], settings.PROJETO_ATUAL)
                nc.add_file(File(file))
                if commit[1] not in autores:
                    autor = Author(commit[1], commit[3])
                    autor.add_commit(nc)
                    autores[commit[1]] = autor

                else:
                    autores[commit[1]].add_commit(nc)
                    autores[commit[1]] = autores[commit[1]]

    return autores
                    

def using_threads(files, regex_list, since, until, git_path=''):
    threads = []
    i = 0
    tat = split_list(regex_list, len(regex_list)/100)
    for t in tat:
        i += 1
        t = threading.Thread(target=extract_commits_regex_by_file, args=(files, t, since, until, i, git_path))
        t.daemon = True
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()

def using_process(files, regex_list, since, until, git_path=''):
    process = []
    methods_list = split_list(regex_list, len(regex_list)/100)
    autores = manager.dict()

    for t in methods_list:
        p = Process(target=extract_commits_regex_by_file, args=(files, t, since, until, autores, git_path))
        p.daemon = True
        p.start()
        process.append(p)
    
    for p in process:
        p.join()

    return dict(autores)

# Busca os commits que possuem referencia às expressões regulares em cada arquivo de uma lista de arquivos
# PRECISA AINDA VERIFICAR SE REALMENTE FAZ REFERENCIA A API, VERIFICAR SE A CLASSE OU MÉTODO É DA API
def commits_regex_by_file(authores_extracted, regex_list, files, since, until, git_path=''):
    print('Buscando commits de arquivos pela lista de metodos.....')

    if not settings.MULTIPROCESSING:
        authores_extracted = extract_commits_regex_by_file(files, regex_list, since, until, authores_extracted, git_path)
    else:
        authores_extracted = using_process(files, regex_list, since, until, git_path)
     # autores = using_threads(files, regex_list, since, until, git_path)
        
    # info_file('output/commits_atributos.txt', id_commit_method)
    # print('Encontrato ' + str(len(commits2)) + ' commits')
    return authores_extracted


def count_commits(autores, project_path):
    
    i = 0
    for key, value in autores.items():
        for key, commit in value.commits.items():
            for file in commit.files:
                entire_commit = run_shell_scripts(get_all_commit(commit.sha1, file.path, project_path), '')
                methods_file = find_patters_commits(entire_commit, settings.LIST_API_METHODS,value.name, settings.CONSIDERAR_REMOCAO)

                file.add_methods(methods_file)

    return autores


def find_your_library(authors_extracted):
    print('Calculando metricas do Find Your Library.....')
    summary = autor_methods_frequency_new(authors_extracted, settings.CONSIDERAR_REMOCAO)
    # autor = autor_methods_frequency(commits, settings.CONSIDERAR_REMOCAO)

    le = library_expertise(settings.LIST_API_METHODS, summary)
    ed = expertise_distance(le)
    find_libray__csv(le, ed)


def expert_recomendation(authors_extracted):
    print("Calculando metricas do Expert Recommendation.....")
    summary = autor_methods_frequency_new(authors_extracted, settings.CONSIDERAR_REMOCAO)

    dm = depth_method(summary)
    bm = breadth_method(summary)
    rd = relative_depth(summary)
    rb = relative_breadth(summary)

    expertise__csv(dm, bm, rd, rb)

def extract_developers(since, until):

    all_files_interest = []
    authors_extracted = {}
    for project in settings.PROJETOS:
        p = project.split('/')
        settings.PROJETO_ATUAL = p[len(p) - 1]
        
        print('Inicando extracao no projeto - '  + settings.PROJETO_ATUAL)

        # Busca os commits que possuiram referencia aos imports
        commits_sh1a = find_commits(settings.LIST_IMPORT_REGEX, since, until, True, project)

        # Busca os arquivos de interesse presentes no commits que possuiam referencia aos import dos
        files_project = get_interest_files(commits_sh1a, settings.LIST_IMPORT_REGEX, project)
        all_files_interest = all_files_interest + files_project

        # Extrai todos os commits que os arquivos de interesse tiveram,
        # buscando os commits que possuem uso dos metodos presentes na lista
        # commits = commits_regex_by_file(list_api_methods, files_interest, project)
        commits_regex_by_file(authors_extracted, settings.LIST_API_METHODS, files_project, settings.SINCE, settings.UNTIL, project)
        count_commits(authors_extracted, project)

    return authors_extracted

def extract_metrics():

    authors_extracted = extract_developers(settings.SINCE, settings.UNTIL)
    complete_summary = summarys(authors_extracted)
    
    small_summary = summary_authors(authors_extracted)

    try:
        tuplas_geral(complete_summary)
        tuplas_resumo(small_summary, 'tuplas_resumo')

        find_your_library(authors_extracted)
        expert_recomendation(authors_extracted)

        return authors_extracted
    except Exception as e:
        print (e)
        logging.warning('0 Commits encontrados no projeto, verifique os parâmetros e api que desejam buscar')
        print('0 Commits encontratos no projeto, verifique os parâmetros e api que desejam buscar')


        

def extract_oraculo__david_ma(before_extracted=None):
    print('\n\n# == BUSCANDO ORÁCULO\n\n')

    since = settings.UNTIL + timedelta(days=1)
    until = settings.UNTIL + timedelta(days=settings.ORACULO_DAVID_MA_DIAS)

    authors_extracted = extract_developers(since, until)
    oraculo_david_ma(before_extracted, authors_extracted)

    
    # tuplas_resumo(small_summary, 'oraculo_david_ma')


def start_extraction():
    print('Iniciando.....')
    settings.init()

    authors_extracted = extract_metrics()
    if settings.ORACULO_DAVID_MA:
        extract_oraculo__david_ma(authors_extracted)