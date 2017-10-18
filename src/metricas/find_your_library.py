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
        expertise = {key: value[key] / provided_symbol.get(key, 0) for key in value.keys()}
        developers[dev] = expertise
    
    return developers


def expertise_distance(library_expertise):
    developers = {}
    for dev, value in library_expertise.iteritems():
        uns = numpy.ones(len(value.values()))
        exp = numpy.array(value.values())
        expertise = numpy.linalg.norm(uns - exp)
        developers[dev] = expertise

    return developers