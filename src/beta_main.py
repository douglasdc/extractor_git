#!/usr/bin/env python3
#coding:utf-8
from subprocess import PIPE, Popen
# from sets import Set
import re, csv, json, logging, timeit, time, os, threading, gc
from multiprocessing import Manager, Process, cpu_count, Value
from datetime import timedelta


from .scripts.run_shell import run_shell_scripts
from .scripts.sh_scripts import *
from .utils import *
from .metricas.find_your_library import library_expertise, expertise_distance
from .metricas.expert_recomendation import depth_method, breadth_method, relative_breadth, relative_depth
from .metricas.metrics import export_expert_recommendation, export_find_your_library
from .parser import *
from .data_manager.data import *
from .data_manager.data_export import *
from .models import Author, Commit, Method, File
from .oraculo import oraculo_david_ma
from . import settings
from collections import Counter

def start_extraction():
    import time
    import datetime
    print('Iniciando.....')
    settings.init()

    autores = {}
    oraculo = {}

    inicio = time.mktime(settings.SINCE.timetuple())
    fim = time.mktime(settings.UNTIL.timetuple())

    inicio_oraculo = time.mktime((settings.UNTIL + timedelta(days=1)).timetuple())
    fim_oraculo = time.mktime((settings.UNTIL + timedelta(days=settings.ORACULO_DAVID_MA_DIAS)).timetuple())

    for project in settings.PROJETOS:
        print(project)
        arquivos_interesse = set()
        commit_hash = run_shell_scripts(tt(project), '')

        commits = commit_hash.split('##--')
        for commit in commits:
            linhas_commit = []
            oraculo_commit = False
            autores_commit = False

            match = re.search(r'^\#\#commit\|(?P<sha1>\w+)\|(?P<author>(\w+\s?)*)\|(?P<timestamp>\d+)\|(?P<email>.+)', commit)
            if match:
                diffs = commit.split('diff')

                commit_dict = match.groupdict()

                new_commit = Commit(commit_dict['sha1'], commit_dict['timestamp'], '')
                valid_commit = False

                for diff in diffs:
                    arquivo_removido = re.search(r'\-\-\-\sa(?P<arquivo_removido>.+.java.+)', diff)
                    if arquivo_removido:
                        arquivo_removido = arquivo_removido.groupdict()['arquivo_removido']

                    arquivo_adicionado = re.search(r'\+\+\+\sa(?P<arquivo_adicionado>.+.java.+)', diff)
                    if arquivo_adicionado:
                        arquivo_removido = arquivo_removido.groupdict()['arquivo_adicionado']
                    if arquivo_adicionado or arquivo_removido:
                        file_name = arquivo_adicionado or arquivo_removido
                        
                        if re.search(r'(\+|\-).+org\.apache\.commons\.io.+', diff) or file_name in arquivos_interesse:
                            arquivos_interesse.add(file_name)
                            time = float(commit_dict['timestamp'])
                            if time >= inicio and time <= fim:
                                autores_commit = True
                                oraculo_commit = False
                                file = File(file_name)
                                methods_calculated = find_patters_commits(diff, settings.LIST_API_METHODS, '', True)
                                valid_commit = valid_commit or methods_calculated != []

                                if valid_commit:
                                    file.add_methods(methods_calculated)
                                    new_commit.add_file(file)

                            if time >= inicio_oraculo and time <= fim_oraculo:
                                oraculo_commit = True
                                autores_commit = False
                                file = File(file_name)
                                methods_calculated = find_patters_commits(diff, settings.LIST_API_METHODS, '', True)
                                valid_commit = valid_commit or methods_calculated != []

                                if valid_commit:
                                    file.add_methods(methods_calculated)
                                    new_commit.add_file(file)
                # print(new_commit.timestamp)
                # print('Autores = ' + str(autores_commit))
                # print('Oraculo = ' + str(oraculo_commit))
                if(autores_commit):
                    if new_commit and commit_dict['author'] not in autores and valid_commit:
                        autores[commit_dict['author']] = Author(commit_dict['author'], commit_dict['email'])
                        autores[commit_dict['author']].add_commit(new_commit)
                    elif new_commit and valid_commit:
                        autores[commit_dict['author']].add_commit(new_commit)

                if(oraculo_commit):
                    if new_commit and commit_dict['author'] not in oraculo and valid_commit:
                        oraculo[commit_dict['author']] = Author(commit_dict['author'], commit_dict['email'])
                        oraculo[commit_dict['author']].add_commit(new_commit)
                    elif new_commit and valid_commit:
                        oraculo[commit_dict['author']].add_commit(new_commit)


    complete_summary = summarys(autores)
    
    small_summary = summary_authors(autores)

    try:
        tuplas_geral(complete_summary)
        tuplas_resumo(small_summary, 'tuplas_resumo')

        export_find_your_library(autores, settings.LIST_API_METHODS, "find_your_library", settings.CONSIDERAR_REMOCAO)
        export_expert_recommendation(autores,"expert_recommendation", settings.CONSIDERAR_REMOCAO)

        # return autores
    except Exception as e:
        print (e)
        logging.warning('0 Commits encontrados no projeto, verifique os parâmetros e api que desejam buscar')
        print('0 Commits encontratos no projeto, verifique os parâmetros e api que desejam buscar')

    print(autores)
    oraculo_david_ma(autores, oraculo)
    print(oraculo)