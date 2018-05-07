#coding:utf-8
# *****************************************************************************
# Implementation of metrics from "Expert Recommendation with Usage Expertise"
# *****************************************************************************

from src.data import methods_total_frequency


# Calcula a profundiade do conhecimento do desenvolvedor
# Consiste na soma da frequencia de uso de todos os métodos da API
# Recebe a frequencia dos métodos para cada desenvolvedor
def depth_method(usage_symbol):
    print('Calculando Depth Method.....')
    developers = {}
    for key, value in usage_symbol.items():
        developers[key] = sum(value.values())

    return developers

# Contagem da quantidade de métodos utilizado pelo desenvolvedor
def breadth_method(usage_symbol):
    print('Calculando Breadth Method.....')
    developers = {}
    for key, value in usage_symbol.items():
        developers[key] = sum(1 for key in value.keys() if value[key] > 0)
    
    return developers

# Calculo da profundidade em relação ao uso de todos os desenvolvedores
def relative_depth(usage_symbol):
    print('Calculando Relative Depth.....')
    total_usage = methods_total_frequency(usage_symbol)
    developers = {}
    for k2, value in usage_symbol.items():
        developers[k2] = sum(float(value[key])/float(total_usage[key]) for key in value.keys())

    return developers

# Caculo da largura relativa em relacao ao uso de todos os desenvolvedores
# Consiste na soma da frequencia relativa para cada metodo da API
def relative_breadth(usage_symbol):
    print('Calculando Relative Breadth.....')
    total_usage = {}
    # for key, value in usage_symbol.items():
    for value in usage_symbol.values():
        for key in value.keys():
            total_usage[key] = total_usage.get(key, 0) + 1

    developers = {}
    for dev, values in usage_symbol.items():
        developers[dev] = sum(1/float(total_usage[key]) for key in values.keys())

    return developers
