#coding:utf-8
from datetime import datetime, date

from ..scripts.run_shell import run_shell_scripts
from ..scripts.sh_scripts import *
from ..models import get_amount_inserted, get_amount_removed, get_frequency_inserted, get_frequency_removed

def summarys(authors):
    from datetime import datetime
    summary = {}
    for key, value in authors.items():
        for key, commit in value.commits.items():
            commit_methods = commit.get_methods()
            files = []
            methods = {}
            for file in commit.files:
                files.append(file.path)
                for method in file.methods:
                    if (method.amount_inserted + method.amount_removed) > 0:
                        tempMethod = {}
                        tempMethod['adicionou'] = method.amount_inserted
                        tempMethod['removeu'] = method.amount_removed

                        methods[method.name] = tempMethod

            tempCommit = {}
            tempCommit['arquivos'] = files
            tempCommit['momento'] = "{:%d %b %Y %H:%M:%S}".format(datetime.fromtimestamp(float(commit.timestamp)))
            tempCommit['email'] = value.email
            tempCommit['timestamp'] = commit.timestamp
            tempCommit['commit'] = commit.sha1
            tempCommit['autor'] = value.name
            tempCommit['metodos'] = methods

            tempCommit['frequencia_inseridos'] = get_frequency_inserted(commit_methods.values())
            tempCommit['frequencia_removidos'] = get_frequency_removed(commit_methods.values())
            tempCommit['frequencia_total'] = tempCommit['frequencia_inseridos'] + tempCommit['frequencia_removidos']
            tempCommit['quantidade_inseridos'] = get_amount_inserted(commit_methods.values())
            tempCommit['quantidade_removidos'] = get_amount_removed(commit_methods.values())
            tempCommit['quantidade_total'] = tempCommit['quantidade_inseridos'] + tempCommit['quantidade_removidos']

            summary[commit.sha1] = tempCommit

    return summary

def summary_authors(authors):
    summary = {}
    for key, value in authors.items():
        author = {}
        methods = {}
        authorMethods = value.get_methods()
        for key, method in authorMethods.items():
            if (method.amount_inserted + method.amount_removed) > 0:
                tempMethod = {}
                tempMethod['adicionou'] = method.amount_inserted
                tempMethod['removeu'] = method.amount_removed

                methods[method.name] = tempMethod
        
        author['frequencia_inseridos'] = get_frequency_inserted(authorMethods.values())
        author['frequencia_removidos'] = get_frequency_removed(authorMethods.values())
        author['frequencia_total'] = author['frequencia_inseridos'] + author['frequencia_removidos']
        author['quantidade_inseridos'] = get_amount_inserted(authorMethods.values())
        author['quantidade_removidos'] = get_amount_removed(authorMethods.values())
        author['quantidade_total'] = author['quantidade_inseridos'] + author['quantidade_removidos']
        author['metodos'] = methods
        author['dev'] = value.name
        author['email'] = value.email

        summary[value.name] = author

    return summary

# Retorna uma lista no formato
# [
#     'Da Vinci':{'metodo': 0, 'metodo': 0},
#     'Mona lisa':{'metodo': 0, 'metodo': 0},
# ]
# Que contem a frequencia de uso de cada método por cada desenvolvedor
def autor_methods_frequency(commits, removed=True):
    autor = {}
    for key, value in commits.items():
        for commit in value.commits.values():
            for file in commit.files:
                for method in file.methods:
                    if key not in autor:
                        autor[key] = {}

                    if method.get_frequency(removed, True) > 0:
                        if method.name not in autor[key]:
                            autor[key][method.name] = 0

                        autor[key][method.name] += method.get_frequency(removed, True)

    return autor

def methods_total_frequency(autor_methods_frequency):
    metodos = {}
    for dev, value in autor_methods_frequency.items():
        for key, uso in value.items():
            metodos[key] = metodos.get(key, 0) + uso
    
    return metodos
