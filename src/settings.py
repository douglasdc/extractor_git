#coding:utf-8
import re, csv, json, logging
from .utils import get_list_lines_from_file

PROJETOS = []
LINGUAGENS = []
PROJETO_ATUAL = []
PROJECT_PATH = ''
CONSIDERAR_REMOCAO = True
REMOVER_LINHAS_IDENTICAS = True
SINCE = ''
UNTIL = ''
ORACULO_DAVID_MA = False
ORACULO_DAVID_MA_DIAS = 0
MULTIPROCESSING = False
IMPORT_FILE = ""
API_FILE = ""

LIST_API_METHODS = []
LIST_IMPORT_REGEX = []

def load_files():
    from datetime import datetime
    global PROJETOS
    global CONSIDERAR_REMOCAO
    global LINGUAGENS
    global REMOVER_LINHAS_IDENTICAS
    global SINCE
    global UNTIL
    global ORACULO_DAVID_MA
    global ORACULO_DAVID_MA_DIAS
    global MULTIPROCESSING
    global IMPORT_FILE
    global API_FILE

    print('Carregando parametros.....')
    try:
        parametros = open('parametros.json')
        parameters = json.load(parametros)
        PROJETOS = parameters['projetos']
        # PROJETOS = projects
        CONSIDERAR_REMOCAO = parameters['considerar_removidos']
        REMOVER_LINHAS_IDENTICAS = parameters['linhas_identicas']
        ORACULO_DAVID_MA = parameters['oraculo_david_ma']
        ORACULO_DAVID_MA_DIAS = parameters['oraculo_david_ma_dias']
        MULTIPROCESSING = parameters['multiprocessing']
        IMPORT_FILE = parameters['import_file']
        API_FILE = parameters['api_file']

        if parameters['code_java']: LINGUAGENS.append('java')
        if parameters['code_python']: LINGUAGENS.append('py')
        if parameters['code_javascript']: LINGUAGENS.append('js')
        if parameters['code_php']: LINGUAGENS.append('php')

        SINCE = datetime.strptime(parameters['data_inicio'], "%Y-%m-%d").date()
        UNTIL = datetime.strptime(parameters['data_fim'], "%Y-%m-%d").date()

    except Exception as ex:
        logging.critical('FALHA NO ARQUIVO DE PARAMETROS')
        print('Verifique seu arquivo de parametros, algo de errado não está certo')


def load_imports():
    global LIST_IMPORT_REGEX

    print('Carregando imports da API.....')
    file_imports = IMPORT_FILE
    LIST_IMPORT_REGEX = get_list_lines_from_file(file_imports)

    print('Imports no arquivo: ' + str(len(LIST_IMPORT_REGEX)))


def load_methods():
    global LIST_API_METHODS

    print('Carregando metodos da API.....')
    file_methods = API_FILE
    LIST_API_METHODS = get_list_lines_from_file(file_methods)

    print('Metodos no arquivo: ' + str(len(LIST_API_METHODS)))


def init():

    load_files()
    load_imports()
    load_methods()

