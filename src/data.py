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
    print 'Summary author.....'
    autores = {}
    for key, value in commits.iteritems():
        if value['autor'] not in autores:
            temp = {}
            temp['dev'] = value['autor']
            temp['metodos'] = value['metodos']
            temp['quantidade_total'] = len(value['metodos'])
            # print(len(value['metodos']))
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

            # autores[value['autor']]['metodos'] = for key, value in value['metodos'].iteritems()
            t = set()
            t = value['metodos'].keys() + autores[value['autor']]['metodos'].keys()
            print len(set(t))
            autores[value['autor']]['quantidade_total'] = len(set(t))
            autores[value['autor']]['quantidade_inseridos'] = autores[value['autor']]['quantidade_inseridos'] + sum(1 for key, value in value['metodos'].iteritems() if value['adicionou'] > 0 and key not in autores[value['autor']]['metodos'].keys())
            autores[value['autor']]['quantidade_removidos'] = autores[value['autor']]['quantidade_total'] - autores[value['autor']]['quantidade_inseridos']

            autores[value['autor']]['frequencia_total'] = autores[value['autor']]['frequencia_total'] + sum(value['adicionou'] + value['removeu'] for key, value in value['metodos'].iteritems())
            autores[value['autor']]['frequencia_inseridos'] = autores[value['autor']]['frequencia_inseridos'] + sum(value['adicionou'] for key, value in value['metodos'].iteritems())
            autores[value['autor']]['frequencia_removidos'] = autores[value['autor']]['frequencia_total'] - autores[value['autor']]['frequencia_inseridos']
    
    return autores

        # value['metodos'] = {key: value for key, value in value['metodos'].iteritems() if (value['adicionou'] + value['removeu']) > 0}
