# Implementation of metrics from "Find Your Library Experts"

# Define o conjunto de simbolos usado pelo desenvolvedor
def symbols_usage():
    return None

# Conjunto de simbolos usados por todos os desenvolvedores    
def provided_symbols():
    return None

# Relação entre o uso de um método pelo desenvolvedor e todo o uso dentro do projeto
def library_expertise(provided_symbol, usage_symbol):
    developers = {}
    for key, value in usage_symbol.iteritems():
        expertise = {key: usage_symbol[key] / provided_symbol.get(key, 0) for key in usage_symbol.keys()}
        developers[key] = expertise
    
    return developers


def expertise_distance():
    return None