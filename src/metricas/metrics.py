#coding:utf-8
from .expert_recomendation import *
from .find_your_library import *
from ..data_manager.data_export import find_libray__csv, expertise__csv
from ..data_manager.data import autor_methods_frequency

def export_expert_recommendation(authors_extracted, file_name, removed=True):
    summary = autor_methods_frequency(authors_extracted, removed)

    dm = depth_method(summary)
    bm = breadth_method(summary)
    rd = relative_depth(summary)
    rb = relative_breadth(summary)

    expertise__csv(dm, bm, rd, rb, file_name)


def export_find_your_library(authors_extracted, api_list, file_name, removed=True):
    summary = autor_methods_frequency(authors_extracted, removed)

    le = library_expertise(api_list, summary)
    ed = expertise_distance(le)
    find_libray__csv(le, ed, file_name)
