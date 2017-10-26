#coding:utf-8

from datetime import datetime

from scripts.run_shell import run_shell_scripts
from scripts.sh_scripts import *

def summary(commits):
    for key, value in commits.iteritems():
        value['metodos'] = {key: value for key, value in value['metodos'].iteritems() if (value['adicionou'] + value['removeu']) > 0}
        value['momento'] = "{:%d %b %Y %H:%M:%S}".format(datetime.fromtimestamp(float(value['timestamp'])))

    return commits


def summary_author(commits):
    autores = {}
    for key, value in commits.iteritems():
        if value['autor'] not in autores:
            temp = {}
            temp['dev'] = value['autor']
            temp['metodos'] = value['metodos']
            temp['quantidade_total'] = len(value['metodos'])
            temp['quantidade_inseridos'] = sum(1 for key, value in value['metodos'].iteritems() if value['adicionou'] > 0)
            temp['quantidade_removidos'] = temp['quantidade_total'] - temp['quantidade_inseridos']
            temp['frequencia_total'] = sum(value['adicionou'] + value['removeu'] for key, value in value['metodos'].iteritems())
            temp['frequencia_inseridos'] = sum(value['adicionou'] for key, value in value['metodos'].iteritems())
            temp['frequencia_removidos'] = temp['frequencia_total'] - temp['frequencia_inseridos']

            autores[value['autor']] = temp

        else:
            for metodo, values in value['metodos'].iteritems():
                if metodo in autores[value['autor']]['metodos']:
                    autores[value['autor']]['metodos'][metodo]['adicionou'] = autores[value['autor']]['metodos'][metodo]['adicionou'] + value['metodos'][metodo]['adicionou']
                    autores[value['autor']]['metodos'][metodo]['removeu'] = autores[value['autor']]['metodos'][metodo]['removeu'] + value['metodos'][metodo]['removeu']
                else:
                    autores[value['autor']]['metodos'][metodo] = values
            
            autores[value['autor']]['quantidade_total'] = len(autores[value['autor']]['metodos'].keys())
            autores[value['autor']]['quantidade_inseridos'] = sum(1 for key, itens in autores[value['autor']]['metodos'].iteritems() if autores[value['autor']]['metodos'][key]['adicionou'] > 0)
            autores[value['autor']]['quantidade_removidos'] = sum(1 for key, itens in autores[value['autor']]['metodos'].iteritems() if autores[value['autor']]['metodos'][key]['removeu'] > 0)

            autores[value['autor']]['frequencia_total'] = autores[value['autor']]['frequencia_total'] + sum(value['adicionou'] + value['removeu'] for key, value in value['metodos'].iteritems())
            autores[value['autor']]['frequencia_inseridos'] = autores[value['autor']]['frequencia_inseridos'] + sum(value['adicionou'] for key, value in value['metodos'].iteritems())
            autores[value['autor']]['frequencia_removidos'] = autores[value['autor']]['frequencia_total'] - autores[value['autor']]['frequencia_inseridos']
    
    return autores

# Retorna uma lista no formato
# [
#     'Da Vinci':{'metodo': 0, 'metodo': 0},
#     'Mona lisa':{'metodo': 0, 'metodo': 0},
# ]
# Que contem a frequencia de uso de cada método por cada desenvolvedor
def autor_methods_frequency(commits, removidos=True):
    autor = {}
    for key, value in commits.iteritems():
        if removidos:
            autor[key] = {k: v['adicionou'] + v['removeu'] for k, v in value['metodos'].iteritems()}
        else:
            autor[key] = {k: v['adicionou'] for k, v in value['metodos'].iteritems()}

    return autor


def methods_total_frequency(autor_methods_frequency, removidos=True):
    metodos = {}
    for dev, value in autor_methods_frequency.iteritems():
        for key, uso in value.iteritems():
            metodos[key] = metodos.get(key, 0) + uso
        
    return metodos
