#coding:utf-8

from datetime import datetime

from .scripts.run_shell import run_shell_scripts
from .scripts.sh_scripts import *
from .models import get_amount_inserted, get_amount_removed, get_frequency_inserted, get_frequency_removed

def summary_method(method):
    
    tempMethod = {}
    if (method.amount_inserted + method.amount_removed) > 0:
        tempMethod['adicionou'] = method.amount_inserted
        tempMethod['removeu'] = method.amount_removed

    return tempMethod
    

def summary(commits):
    from datetime import datetime
    for key, value in commits.items():
        value['metodos'] = {keys: values for keys, values in value['metodos'].items() if (values['adicionou'] + values['removeu']) > 0}
        value['momento'] = "{:%d %b %Y %H:%M:%S}".format(datetime.fromtimestamp(float(value['timestamp'])))

    # print(commits)
    return commits

def summarys(authors):
    summary = {}
    from datetime import datetime
    for key, value in authors.items():
        for commit in value.commits:
            # print(len(value.commits))
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

            summary[commit.sha1] = tempCommit

            # print(commit.sha1)

    # print(summary)
    return summary
                    

def summary_author(commits):
    autores = {}
    for key, value in commits.items():
        if value['autor'] not in autores:
            temp = {}
            temp['dev'] = value['autor']
            temp['metodos'] = value['metodos']
            temp['email'] = value['email']
            temp['quantidade_total'] = len(value['metodos'])
            temp['quantidade_inseridos'] = sum(1 for key, value in value['metodos'].items() if value['adicionou'] > 0)
            temp['quantidade_removidos'] = temp['quantidade_total'] - temp['quantidade_inseridos']
            temp['frequencia_total'] = sum(value['adicionou'] + value['removeu'] for key, value in value['metodos'].items())
            temp['frequencia_inseridos'] = sum(value['adicionou'] for key, value in value['metodos'].items())
            temp['frequencia_removidos'] = temp['frequencia_total'] - temp['frequencia_inseridos']

            autores[value['autor']] = temp

        else:
            for metodo, values in value['metodos'].items():
                if metodo in autores[value['autor']]['metodos']:
                    autores[value['autor']]['metodos'][metodo]['adicionou'] = autores[value['autor']]['metodos'][metodo]['adicionou'] + value['metodos'][metodo]['adicionou']
                    autores[value['autor']]['metodos'][metodo]['removeu'] = autores[value['autor']]['metodos'][metodo]['removeu'] + value['metodos'][metodo]['removeu']
                else:
                    autores[value['autor']]['metodos'][metodo] = values
            
            autores[value['autor']]['quantidade_total'] = len(autores[value['autor']]['metodos'].keys())
            autores[value['autor']]['quantidade_inseridos'] = sum(1 for key, itens in autores[value['autor']]['metodos'].items() if autores[value['autor']]['metodos'][key]['adicionou'] > 0)
            autores[value['autor']]['quantidade_removidos'] = sum(1 for key, itens in autores[value['autor']]['metodos'].items() if autores[value['autor']]['metodos'][key]['removeu'] > 0)

            autores[value['autor']]['frequencia_total'] = autores[value['autor']]['frequencia_total'] + sum(value['adicionou'] + value['removeu'] for key, value in value['metodos'].items())
            autores[value['autor']]['frequencia_inseridos'] = autores[value['autor']]['frequencia_inseridos'] + sum(value['adicionou'] for key, value in value['metodos'].items())
            autores[value['autor']]['frequencia_removidos'] = autores[value['autor']]['frequencia_total'] - autores[value['autor']]['frequencia_inseridos']
    
    print(autores)
    return autores

def summary_authors(authors):
    summary = {}
    from datetime import datetime
    for key, value in authors.items():
        author = {}
        methods = {}
        authorMethods = value.get_methods()
        # if value.name == 'oyevstafyev':
        #     print(authorMethods['equals'].amount_inserted)
        #     print(authorMethods['or'].amount_inserted)
        for key, method in authorMethods.items():
            if (method.amount_inserted + method.amount_removed) > 0:
                tempMethod = {}
                tempMethod['adicionou'] = method.amount_inserted
                tempMethod['removeu'] = method.amount_removed

                methods[method.name] = tempMethod
        
        # author['frequencia_inseridos'] = get_frequency_inserted(authorMethods.values())
        # author['frequencia_removidos'] = get_frequency_removed(authorMethods.values())
        # author['quantidade_inseridos'] = get_amount_inserted(authorMethods.values())
        # author['quantidade_removidos'] = get_amount_removed(authorMethods.values())
        author['metodos'] = methods
        author['dev'] = value.name
        author['email'] = value.email

        # print(author)


        # for commit in value.commits:
        #     commit.get_methods()
            # print(len(value.commits))
            # files = []
            # methods = {}
            # for file in commit.files:
            #     print(file.methods)
        
    return {}


# Retorna uma lista no formato
# [
#     'Da Vinci':{'metodo': 0, 'metodo': 0},
#     'Mona lisa':{'metodo': 0, 'metodo': 0},
# ]
# Que contem a frequencia de uso de cada método por cada desenvolvedor
def autor_methods_frequency(commits, removidos=True):

    autor = {}
    for key, value in commits.items():

        if removidos:
            autor[key] = {k: v['adicionou'] + v['removeu'] for k, v in value['metodos'].items()}
        else:
            autor[key] = {k: v['adicionou'] for k, v in value['metodos'].items()}

    return autor


def methods_total_frequency(autor_methods_frequency):
    metodos = {}
    for dev, value in autor_methods_frequency.items():
        for key, uso in value.items():
            metodos[key] = metodos.get(key, 0) + uso
    
    return metodos
