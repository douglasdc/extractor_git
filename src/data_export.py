#coding:utf-8
from .utils import *

def tuplas_geral(commits_summary):
    temp = []
    for c in commits_summary.values():
        for key, value in c['metodos'].items():
            a = c.copy()
            del a['metodos']
            del a['arquivos']
            a['metodo'] = key
            a['adicionou'] = value['adicionou']
            a['removeu'] = value['removeu']
            temp.append(a)
    
    write_csv('output', 'tuplas_extraidas', temp)

    return temp

def tuplas_resumo_commit(commits_summary, file_name):
    temp = []
    for c in commits_summary.values():
        a = c.copy()
        del a['metodos']
        del a['arquivos']
        a['metodo'] = ' | '.join(map(str, c['metodos'].keys()))
        
        temp.append(a)
    
    temp = sorted(temp, key = lambda x: x['timestamp'])
    
    write_csv('output', file_name, temp)
    
    return temp

def tuplas_resumo(commits_author, file_name):
    temp = []
    for key, value in commits_author.items():
        autor = value.copy()
        autor['metodos'] = ' | '.join(map(str, autor['metodos'].keys()))
        autor['desenvolvedor'] = autor.pop('dev')
        autor['email'] = autor.pop('email')
        temp.append(autor)

    write_csv('output', file_name, temp)

    return temp

def find_libray__csv(library_expertise, expertise_distance):
    developers = []
    for dev, value in library_expertise.items():
        temp = {}
        temp['exp_dist'] = expertise_distance[dev]
        temp['desenvolvedor'] = dev
        temp['lib_exp'] = value
        developers.append(temp)

    write_csv('output', 'find_your_library', developers)


def expertise__csv(depth_method, breadth_method, relative_depth, relative_breadth):
    developers = []
    for dev in depth_method.keys():
        temp = {} 
        temp['dev'] = dev  
        temp['depth'] = depth_method[dev]
        temp['breadth'] = breadth_method[dev]
        temp['relative_depth'] = relative_depth[dev]
        temp['relative_breadth'] = relative_breadth[dev]

        developers.append(temp)
    
    write_csv('output', 'expert_recommendation', developers)
