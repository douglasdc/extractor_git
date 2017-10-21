#coding:utf-8
# Implementation of metrics from "Expert Recommendation with Usage Expertise"

# Calcula a profundiade do conhecimento do desenvolvedor
# Consiste na soma da frequencia de uso de todos os métodos da API
# Recebe a frequencia dos métodos para cada desenvolvedor
def depth_method(usage_symbol):
    developers = {}
    for key, value in usage_symbol.iteritems():
        developers[key] = sum(value.values())

    return developers

# Contagem da quantidade de métodos utilizado pelo desenvolvedor
def breadth_method(usage_symbol):
    developers = {}
    for key, value in usage_symbol.iteritems():
        developers[key] = sum(1 for key in value.keys() if value[key] > 0)
    
    return developers

# Calculo da profundidade em relação ao uso de todos os desenvolvedores
def relative_depth(total_usage, usage_symbol):
    developers = {}
    for k2, value in usage_symbol.iteritems():
        developers[k2] = sum(float(value[key])/float(total_usage[key]) for key in value.keys())

    return developers

# Caculo da largura relativa em relacao ao uso de todos os desenvolvedores
# Consiste na soma da frequencia relativa para cada metodo da API
def relative_breadth(usage_symbol):
    total_usage = {}
    # for key, value in usage_symbol.iteritems():
    for value in usage_symbol.values():
        for key in value.keys():
            total_usage[key] = total_usage.get(key, 0) + 1

    developers = {}
    for dev, values in usage_symbol.iteritems():
        developers[dev] = sum(1/float(total_usage[key]) for key in values.keys())

    return developers
