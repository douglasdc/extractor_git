#coding:utf-8
from subprocess import PIPE, Popen
from src.scripts.run_shell import run_shell_scripts
from src.scripts.sh_scripts import *
from sets import Set
import re, csv, json, logging, string
# import csv
# import json
# import logging

def main():
    parametros = open('parametros.json')
    parameters = json.load(parametros)
    projects = parameters['projetos']
    print 'TESTE DE SCRIPTS'
    for project in projects:
        commit = run_shell_scripts(get_all_commit('48f315e6626f59c18c1a745def850159a68087be', 'main.java', project), '')

        count_insert = 0
        count_remove = 0
        abs_metodo = 0
        for line in commit.split('\n'):
            if string.find(line, '+', 0, 1) != -1:
                count_insert = count_insert + len(re.findall('.info\(', line))
            
            if string.find(line, '-', 0, 1) != -1:
                count_remove = count_insert + len(re.findall('.info\(', line))

        print count_insert
        print count_remove
if __name__ == "__main__":
    main()
