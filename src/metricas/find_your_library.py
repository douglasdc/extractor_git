#coding:utf-8
# Implementation of metrics from "Find Your Library Experts"

import numpy

# Relação entre o uso de um método pelo desenvolvedor e todo o uso dentro do projeto
# A entrada são duas listas, uma contendo todos os métodos fornecidos pela biblioteca, e outra com os métodos usados por cada desenvolvedor
# provided_symbol = {metodo: quantidade_uso}
# usage_symbol = {dev:{metodo:quantidade_usada}}
def library_expertise(provided_symbol, usage_symbol):
    developers = {}
    for dev, value in usage_symbol.iteritems():
        developers[dev] = sum(1 for v in value.values() if v > 0) /float(len(provided_symbol))
        # expertise = {key: 0.0 if float(provided_symbol.get(key, 0)) == 0 else round(float(
        #     value.get(key, 0)) / float(provided_symbol.get(key, 0)), 4) for key in provided_symbol.keys()}
        # developers[dev] = expertise
    
    return developers


def expertise_distance(library_expertise):
    developers = {}
    # print library_expertise
    for dev, value in library_expertise.iteritems():
        uns = numpy.ones(1)
        exp = numpy.array(value)
        expertise = numpy.linalg.norm(uns - exp)
        developers[dev] = expertise

    return developers
