#coding:utf-8
import string, re, regex

def find_patters_commit(commit, metodos, remove_lines_iquals):
    re_metodos = r'.' + '\(|.'.join(map(str, metodos)) + '\('
    # print re_metodos
    inseridos = [re.sub('\+\s+', '', value) for value in commit.split('\n') if re.search(re_metodos, value) and re.search(r'^\+\s+', value)]
    removidos = [re.sub('\-\s+', '', value) for value in commit.split('\n') if re.search(re_metodos, value) and re.search(r'^\-\s+', value)]

    if remove_lines_iquals:
        for value in inseridos:
            if value in removidos and len(value) > 0:
                inseridos.remove(value)
                removidos.remove(value)

    contagem = {}
    for metodo in metodos:
        contagem[metodo] = {}
        contagem[metodo]['adicionou'] = sum(1 for value in inseridos if re.search(r'.' + metodo + '\(', value))
        contagem[metodo]['removeu'] = sum(1 for value in removidos if re.search(r'.' + metodo + '\(', value))
    
    # print contagem
    return contagem
