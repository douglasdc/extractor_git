#coding:utf-8
from subprocess import PIPE, Popen
from run_shell import run_shell_scripts
from sh_scripts import *
from sets import Set
import re
import xlwt

files_interest = set()
list_import_regex = []
list_api_methods = []
id_commit_method = {}

DEV_COMMIT = {}
DEV_METHOD = {}


def new_file_interest(path):
    return files_interest.append(path)

def get_list_lines_from_file(file_imports):
    linhas = None
    with open(file_imports) as f:
        linhas = f.readlines()

    return [x.strip() for x in linhas] 

# Busca os commits que possuem referencia às expressões regulares de uma lista
def find_commits(list_regex, only_id=False):
    result = []
    for regex in list_regex:
        if only_id:
            ids = run_shell_scripts(commit_sha1_by_regex(regex), '')
            result = result + ids.split('\n')

    return result

def get_commited_files(file_type, sh1a=None):
    if sh1a:
        return run_shell_scripts(commited_files(sh1a, file_type), '')
        
    else:
        return run_shell_scripts(see_changed_files(file_type), '')

# Busca arquivos que possuiram algum commit contendo refrencias a expressoes regulares presentes em uma lista
def get_interest_files(commits_sh1a, regex_list):
    for sh1a in commits_sh1a:
        files = get_commited_files('java', sh1a)
        files = files.split('\n')
        for file_path in files:
            if len(file_path) > 0 and file_path not in files_interest:
                with open(file_path) as f:
                    for regex in regex_list:
                        if(re.search(regex, f.read())):
                            # Insere os arquivos de cada commit na lista de arquivos de interesse
                            files_interest.add(file_path)


# Busca os commits que possuem referencia às expressões regulares em cada arquivo de uma lista de arquivos
# PRECISA AINDA VERIFICAR SE REALMENTE FAZ REFERENCIA A API, VERIFICAR SE A CLASSE OU MÉTODO É DA API
def get_commits_regex_by_file(regex_list, files):
    # id_commit_method = {}
    for file in files:
        for regex in regex_list:
            # id dos commits com uso da expressão para o arquivo
            sh1a = run_shell_scripts(commit_sha1_by_regex_file(regex, file), '')

            if len(sh1a) > 0:
                if sh1a not in id_commit_method:
                    id_commit_method[sh1a] = []
                
                # Insere a expressão na lista das expressoes alteradas por aquele commit
                id_commit_method[sh1a].append(regex)

# Novo desenvolvedor relacionado com o commit, metodos alterados (inseridos, removidos) no commit 
# e o momento em que o commit foi feito
def new_dev_commit(dev, commit, method, timestamp):
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

# Extrai as informações do commit, autor, timestamp(UNIX)
def extract_info_commit(id_commit):
    # for id in id_commit:
    author = run_shell_scripts(author_commit_sha1(id_commit), '')
    timestamp = run_shell_scripts(timestamp_commit_sha1(id_commit), '')
    methods = []
    new_dev_commit(author, id_commit, id_commit_method[id_commit], timestamp )
    for method in id_commit_method[id_commit]:
        new_dev_method(author, method, 1)

def out_dev_data(list_api_methods):
    wb= xlwt.Workbook()
    ws = wb.add_sheet("DEV_METHOD")

    i = 1
    for regex in list_api_methods:
        ws.write(0, i, regex) 
        i = i + 1

    i = 1
    for dev in DEV_METHOD:
        ws.write(i, 0, dev)
        for method in DEV_METHOD[dev]:
            ws.write(i, list_api_methods.index(method) + 1, DEV_METHOD[dev][method])
        i = i + 1


    # ws2 = wb.add_sheet('DEV_COMMIT')
    wb.save("EXTRACTED_DATA.xls")

# print run_shell_scripts(all_contribuitors_name, '')
def main():
    print 'COMEÇANDO :D'

    file_imports = 'imports.txt' # Arquivo com padrões do import da api desejada
    file_methods = 'log4j.txt' # Arquivo com os padrões das chamadas de métodos
    list_import_regex = get_list_lines_from_file(file_imports) # Converte o arquivo em lista
    list_api_methods = get_list_lines_from_file(file_methods) # Converte o arquivo em lista
    print len(list_api_methods)
    # Busca os commits que possuiram referencia aos imports
    commits_sh1a = find_commits(list_import_regex, True)
    
    # Busca os arquivos de interesse presentes no commits que possuiam referencia aos import dos 
    get_interest_files(commits_sh1a,list_import_regex)

    # Extrai todos os commits que os arquivos de interesse tiveram, 
    # buscando os commits que possuem uso dos metodos presentes na lista
    get_commits_regex_by_file(list_api_methods, files_interest)

    # print id_commit_method
    for commit in id_commit_method:
        extract_info_commit(commit)

    out_dev_data(list_api_methods)


if __name__ == "__main__":
    main()