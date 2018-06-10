#coding:utf-8
import string, re, regex
from .models import Method

def find_patters_commit(commit, metodos, remove_lines_iquals):
    re_metodos = r'.' + '\(|.'.join(map(str, metodos)) + '\('

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
    
    return contagem

def find_patters_commits(entire_commit, methods, value, remove_lines_equals=True):
    re_methods = r'.' + '\(|.'.join(map(str, methods)) + '\('

    inserted = [re.sub('\+\s+', '', value) for value in entire_commit.split('\n') if re.search(re_methods, value) and re.search(r'^\+\s+', value)]
    removed = [re.sub('\-\s+', '', value) for value in entire_commit.split('\n') if re.search(re_methods, value) and re.search(r'^\-\s+', value)]

    if remove_lines_equals:
        for value in inserted:
            if value in removed and len(value) > 0:
                inserted.remove(value)
                removed.remove(value)

    quantified_methods = []
    for method in methods:
        amount_inserted = sum(1 for value in inserted if re.search(r'.' + method + '\(', value))
        amount_removed = sum(1 for value in removed if re.search(r'.' + method + '\(', value))
       
        m = Method(method, '', amount_inserted, amount_removed, 0, 0)
        
        if amount_inserted + amount_removed > 0:
            quantified_methods.append(m)

    return quantified_methods
