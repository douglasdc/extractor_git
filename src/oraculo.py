#coding:utf-8
import os

from .data import *
from .data_export import *
from .models import *
from .utils import delete_files

def oraculo_david_ma(before_extracted, authors_extracted):
    folder = 'oraculo'
    path = 'output/' + folder
    if not os.path.exists(path):
        os.makedirs(path)

    delete_files(path)

    # Extracao do resumo do oraculo pelos commits feitos no período definido para extração do oráculo
    summary = summarys(authors_extracted)
    tuplas_resumo_commit(summary, 'oraculo_david_ma')

    all_commits = {}
    for key, value in authors_extracted.items():
        all_commits.update({x.timestamp:{'author':key, 'commit':x} for x in value.commits.values()})
    
    i = 0
    sorted_commits = sorted(all_commits.items(), key= lambda x: x[0])
    for commit in sorted_commits:
        i+=1
        if commit[1]['author'] not in before_extracted:
            name = authors_extracted[commit[1]['author']].name
            email = authors_extracted[commit[1]['author']].email
            before_extracted[commit[1]['author']] = Author(name, email)

        before_extracted[commit[1]['author']].add_commit(commit[1]['commit'])
        
        small_summary = summary_authors(before_extracted)
        tuplas_resumo(small_summary, folder + '/' + str(i) + '_' + commit[1]['author'] + '_oraculo David Ma')
